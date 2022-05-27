import socket, os, time, tools, users, threading, json, aes
from game import Game
from time import time

def exit():
    """end server at any time  by entering exit"""
    while True:
        inp = input()
        if inp == "exit":
            os._exit(0)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip, port = "127.0.0.1", 65000
server.bind((ip, port))
server.listen(1)

print(f"Server listening on {ip}:{port}")
signup_ip = {}

ciphering = aes.AESCipher("DWKLAJWKLJWKAJDKLNkdnajkwnd23")

class Instance:
    """Named Instance because this is an instance of a player in a Game()"""
    def __init__(self, client, addr):
        """client arg here is client var assigned from server.accepet()"""
        
        # init here to keep some track of vars
        # self.game defined further either at signin, load game
        self.client = client  # for better access across class
        self.ip = addr[0]  # identification
        self.username = "<NUL>"
        self.input_functions = {
            # user functions here
            "signin": self.signin,
            "signup": self.signup,

            # set to return an error unless signed in
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
            "code0008:f": "incorrect number of args",
            "code0009:f": "invalid input",
        }

        self.data_stream()  # a loop where client and server communicates

    def data_stream(self):
        """main function of this class
        a loop where client and server can communicate in turn"""
        while True:
            # message from client
            try:
                info = self.client.recv(1024)
            except ConnectionResetError:
                print(f"{self.ip} has forcibly closed connection")
                break

            # decrypt
            info = ciphering.decrypt(info)

            # turn the message from client into a list form management
            args = tools.separator(info)
            self.print_args(args)

            try:
                # this is string wich maps to the function at self.input_functions
                function_string = args[0]
            except IndexError:
                # incase user send message without any letters
                self.client.send("code0006:f".encode("utf-8"))

            # if function_string == "break":
            #     break

            try:
                # get memory location of the needed function
                function = self.input_functions[function_string]
            except KeyError:
                # the key is not in dict return an error to user
                # continue statements skip all the code below it
                self.client.send("code0005:f".encode("utf-8"))
                continue

            # enter the list of args into the function and store it in a var 
            response = function(args)

            # encrypt
            response = ciphering.encrypt(response)

            try:
                # send response to the user
                self.client.send(response)
            except AttributeError:
                # some functions do not return a value therefore the above line
                # raises an error
                pass

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
            "new_game": self.new_game
            })

        self.username = userName  # set the username public

        self.savefile = f"{userName}.json"
        self.new_game()
        
        try:
            # try opening the savefile
            with open(self.savefile, 'r') as f:
                # load all games from disk to memory
                save_game = json.load(f)
        except FileNotFoundError:
            # if no such file new_game is called and game.__dict__will not be empty
            new_game()
        else:
            # if no eerror save the things in file to main dict
            self.game.__dict__ = save_game
        finally:
            return "code0004:s"  # sucessfully logged in

    def print_args(self, args):
        for r in args:
            print(r, end=" ")

    def print_response(self, func, response):
        print(f"{func}: {self.responses[response]}")

    def signup(self, args):
        global ipdata

        if len(args) != 3:
            return "code0001:f"

        username = args[1]
        password = args[2]
        
        with open("users.json", 'r') as f:
            data = json.load(f)

        try:
            ipdata = signup_ip[self.ip]
        except KeyError:
            pass
        else:
            last_time = ipdata[1]
            if (time() - last_time) < 1800:
                return "code0001:a"
        
        timestamp = time()
        
        try:
            data[username]
        except KeyError:
            data.update({username: password})
            with open("users.json", 'w') as f:
                json.dump(data, f)
            
            signup_ip.update({self.ip: [username, timestamp]})
            return "code0001:s"
        else:
            return "code0001:i"

    def new_game(self, args=[]):
        """function to create a new game"""
        self.game = Game(self.username)  # init game
        self.save_game()  # save new game to disk

        return "code0007:s"

    def save_game(self):
        """function save game"""
        with open(self.savefile, 'w') as f:
            json.dump(self.game.__dict__, f)
        
    def dummy(self, args=[]):
        # this is a dummy function that returns an error code
        return "code0009:f"
    
    def output(self):
        pass
    
    def change_level(self, args):
        """function to check args and change level"""
        if len(args) != 2:
            return "code0007:f"
        
        inp = args[1] 
        
        response = game.update_level(inp)
        return response
    
    def submit(self, args):
        if len(args) != 2:
            return "code0008:f"
        
        response = game.submit(args[1])
        return response

if __name__ == "__main__":
    t = threading.Thread(target=exit)
    t.start()  # classic thrading       

    while True:
        client, addr = server.accept()
        Instance(client, addr)
