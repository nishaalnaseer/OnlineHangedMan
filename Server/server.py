import socket, os, tools, users, threading, json
from game import Game
from time import time
from datetime import datetime

if os.name == "nt":
    slash = '\\'
else:
    slash = '/'

def exit():
    """end server at any time  by entering exit"""
    while True:
        inp = input()
        if inp == "exit":
            os._exit(0)

ip, port = "127.0.0.1", 65000
            
class Instance:
    """Named Instance because this is an instance of a player in a Game()"""
    def __init__(self, client, addr):
        """client arg here is client var assigned from server.accepet()"""

        # init here to keep some track of vars
        # self.game defined further either at signin, load game
        self.client = client  # for better access across class
        self.ip = addr[0]  # identification with user creations
        self.id = self.ip  # for identification, is equated to username after signin
        self.cport = addr[1]
        self.block_counter = 0
        self.big_block_counter = 0
        self.username = "<<NUL>>"
        self.input_functions = {
            # user functions here
            "signin": self.signin,
            "signup": self.signup,

            "hi_scos": self.return_hi_scos,

            # set to return an error code unless signed in
            # game function below only available after signin
            "new_game": self.dummy,
            "submit": self.dummy,
            "level": self.dummy,
            }
        self.responses = {
            "code0000:f": "no spaces in username or password allowed",
            "code0001:f": "incorrect number of args",
            "code0001:i": "username already taken",
            "code0001:s": "sucessfully signed up",
            "code0001:a": "created too many users for now",
            "code0002:f": "username not on file",
            "code0003:f": "username or password missing",
            "code0000:m": "no spaces in username or password allowed",
            "code0004:c": "client password wrong",
            "code0004:s": "sucessfully logged in",
            "code0004:p": "sucessfully signed up",
            "code0004:i": "insufficient args",
            "code0004:j": "too many args",
            "code0004:u": "username not on file",
            "code0005:f": "incorrect input (no funncion that matches)",
            "code0006:f": "no input",
            "code0007:s": "New Game",
            "code0007:f": "incorrect number of args",
            "code0007:a": "zerodivison error",
            "code0007:b": "ValueError prolly str with char to int",
            "code0008:f": "incorrect number of args",
            "code0009:f": "user has not signed in",
            "code0010:g": "player is dead need to start a new_game",
            "code0010:g": "player just died",
        }

        self.data_stream()  # a loop where client and server communicates

    def data_stream(self):
        """main function of this class
        a loop where client and server can communicate in turn"""
        global blocked_ips
        while True:
            # message from client
            try:
                info = self.client.recv(1024).decode("utf-8")
            except ConnectionResetError:
                print(f"{self.id} has forcibly closed connection")
                try:
                    self.save_game()
                except AttributeError:
                    self.blocker(code="code0012:a", info="no info ConnectionResetError")
                    break
                break
            except ConnectionAbortedError:
                print(f"{self.id} has forcibly closed connection")
                self.save_game()
                break

            info = info.replace('\n', '')
            info = info.replace('\r', '')

            # turn the message from client into a list form management
            args = tools.separator(info)
            self.print_args(args)

            try:
                # this is string wich maps to the function at self.input_functions
                function_string = args[0]
            except IndexError:
                # incase user send message without any letters
                self.blocker(code="code0006:f", info=info)

                self.client.send("code0006:f\n".encode("utf-8"))
                # self.print_response("code0006:f", "code0006:f")
                if self.block_counter == 5 or self.big_block_counter == 100:
                    break

                continue

            try:
                # get memory location of the needed function
                function = self.input_functions[function_string]
            except KeyError:
                # the key is not in dict return an error to user
                # continue statements skip all the code below it
                self.blocker(code="code0005:f", info=info)

                self.client.send("code0005:f\n".encode("utf-8"))
                
                if self.block_counter == 5 or self.big_block_counter == 100:
                    break

                continue
            else:
                self.block_counter = 0

            # enter the list of args into the function and store it in a var 
            response = function(args)

            try:
                # send response to the user
                self.client.send(f"{response}\n".encode("utf-8"))
            except AttributeError:
                # some functions do not return a value therefore the above line
                # raises an error
                pass

            try: 
                self.print_response(function_string, response)
            except KeyError:
                print("Sent: '" + response + "' to " + self.id)

    def signin(self, args):
        """password and username in a list to login"""

        if len(args) > 3:
            # if lenght is more than 3 return an error code
            # if user sends a username or password with spaces
            return "code0004:j"
        elif len(args) < 3:
            return "code0004:i"

        try:
            userName = args[1]
            password = args[2]
        except IndexError:
            # user sends a username and or pass as an empty string
            return "code0004:i"

        users_on_file = users.loadUsers()  # load all users saved on file

        try: 
            # get user password
            passwordOnFile = users_on_file[userName]
        except TypeError:
            # if file is empty of null
            return "code0004:u"
        except KeyError:
            # if user is missing return an error code
            return "code0004:u"

        if password != passwordOnFile:
            # if password entered doesnt match
            return "code0004:c"  # prevent below code execution

        self.input_functions.update({
            # if user is signed in update the dict to allow game funcitons
            "new_game": self.new_game,
            "level": self.change_level,
            "submit":self.submit,
            })

        self.username = userName  # set the username public
        self.id = userName  # console idenification

        self.savefile = f"user_files{slash}{userName}.json"
        # self.new_game()

        try:
            # try opening the savefile
            with open(self.savefile, 'r') as f:
                # load all games from disk to memory
                save_game = json.load(f)
            if save_game["dead"] == False:
                self.new_game()
                self.game.__dict__ = save_game
            if self.hi_sco < save_game["score"]:
                self.hi_sco = save_game["score"]
        except FileNotFoundError:
            # if no such file new_game is called and game.__dict__will not be empty
            self.hi_sco = 0
            self.new_game()
        finally:
            # if no eerror save the things in file to main dict

            with open("hi-scos.json", 'r') as f:
                scores = json.load(f)
            self.hi_sco = scores[userName]
            return f"code0004:s {self.game.progress} {self.game.score} {self.hi_sco} {self.game.count} {self.game.level}"# sucessfully logged in

    def print_args(self, args):
        statement = f"Recieved from {self.id}: "
        for r in args:
            statement += r + " "
        statement = statement[:-1]
        print(statement + "'")

    def print_response(self, func, response):
        statement = f"Function: {func} - Sent: '{self.responses[response]}' to {self.id}"
        print(statement)

    def signup(self, args):
        """function to create new user"""
        global ipdata  # information about ips and their last user creation

        if len(args) != 3:
            return "code0001:f"

        username = args[1]
        password = args[2]

        with open("users.json", 'r') as f:
            data = json.load(f)  #load old data

        try:
            ipdata = signup_ip[self.ip]
        except KeyError:
            # if key error then this is the first time this ip is creating a user
            pass
        else:
            # else and time is less than 30 minutes return an error code
            last_time = ipdata[1]
            if (time() - last_time) < 1800:
                return "code0001:a"

        timestamp = time()  # get cuurennt timestamp if user is being created

        try:
            data[username]
        except KeyError:
            # if keyerror then this is the first time this ip is being used to create a user
            data.update({username: password})
            with open("users.json", 'w') as f:
                json.dump(data, f)

            signup_ip.update({self.ip: [username, timestamp]})  # save

            with open("hi-scos.json", 'r') as f:
                scores = json.load(f)
            scores.update({username: 0})

            with open("hi-scos.json", 'w') as f:
                json.dump(scores, f)


            return "code0001:s"
        else:
            return "code0001:i"

    def new_game(self, args=[]):
        """function to create a new game"""
        self.game = Game(self.username)  # reinit game
        self.input_functions.update({
            # if user is signed in update the dict to allow game funcitons
            "level": self.change_level,
            "submit": self.submit,
            })

        self.save_game()  # save new game to disk

        return f"new_game {self.game.progress}"

    def save_game(self):
        """function save game"""
        with open(self.savefile, 'w') as f:
            json.dump(self.game.__dict__, f)

        try:
            self.hi_sco
        except AttributeError:
            self.hi_sco = 0

        # print(f"this is working hi score is {self.hi_sco} score is {self.game.score}") # debug

        if self.game.score > self.hi_sco:
            self.hi_sco = self.game.score
            with open("hi-scos.json", 'r') as f:
                scores = json.load(f)
            scores.update({self.username: self.hi_sco})

            with open("hi-scos.json", 'w') as f:
                json.dump(scores, f)

    def dummy(self, args=[]):
        # this is a dummy function that returns an error code
        return "code0009:f"

    def dead(self, args=[]):
        return "code0010:a"

    def change_level(self, args):
        """function to check args and change level"""
        if len(args) != 2:
            return "code0007:f"

        inp = args[1] 

        response = self.game.update_level(inp)
        return response

    def submit(self, args):
        if len(args) != 2:
            return "code0008:f"

        response = self.game.event(args[1])
        print(f"Real word of {self.id}: {self.game.random_word}")

        if self.game.dead == True:

            self.input_functions.update({
                # if user is signed in update the dict to allow game funcitons
                "level": self.dead,
                "submit": self.dead,
                })
            return f"code0010:g {self.game.score} {self.game.random_word}"

        self.save_game()
        return response

    def return_hi_scos(self, args=[]):
        with open("hi-scos.json", 'r') as f:
            scores = json.load(f)

        keys_to_send = ""
        values_to_send = ""
        k_len = len(scores.keys())
        data = dict(sorted(scores.items(), key=lambda items : items[1]))

        for k, v in data.items():
            keys_to_send += f"{k} "
            values_to_send += f"{v} "

        return f"scores {keys_to_send}{values_to_send}{k_len}"

    def blocker(self, code, info):
        self.block_counter += 1
        self.big_block_counter += 1
        now = datetime.now()

        if self.block_counter == 6 or self.big_block_counter == 100:
            code = "code0011:a\n"
            self.client.send(code.encode("utf-8"))
            blocked_ips.append(self.ip)
            now = datetime.now()

            with open("log.txt", 'a') as f:
                f.write(f"{now} {self.ip} has been blocked!\n")
                print(f"{self.ip} has been blocked!")
        
        log_statement = f"{now} {self.id} - received: '{info}' sent: '{code}'"
        log_statement += f" block_counter: {self.block_counter}"
        print(log_statement)
        log_statement += "\n"
        with open("log.txt", 'a') as f:
            f.write(log_statement)

if __name__ == "__main__":
    t = threading.Thread(target=exit)
    t.start()  # classic thrading

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)

    print(f"Server listening on {ip}:{port}")
    signup_ip = {}
    blocked_ips = []

    while True:
        client, addr = server.accept()

        # if addr[0] in blocked_ips:
        #     continue

        # try:
        #     client.send("ok".encode("utf-8"))
        #     client.send("code0006:f\n".encode("utf-8"))
        # except e:
        #     print(e)
        #     continue

        Instance(client, addr)
