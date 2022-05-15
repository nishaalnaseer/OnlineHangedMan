import socket, os, time, tools, users, threading
from game import Game

def exit():
    inp = input()
    if inp == "exit":
        os._exit(0)

t = threading.Thread(target=exit)
t.start()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip, port = "127.0.0.1", 65000
server.bind((ip, port))
server.listen(1)

print(f"Server listening on {ip}: {port}")

class Instance():
    def __init__(self, client):
        self.games = {}
        self.client = client
        self.input_functions = input_functions = {
            "signin": self.signin,  
            "signup": users.signup,

            # "new_game": new_game
            }
        self.data_stream()

    def data_stream(self):
        while True:
            info = self.client.recv(1024).decode("utf-8")

            args = tools.separator(info)
            print(args)

            function_string = args[0]
            try:
                if args[0] == "break":
                    break
            except IndexError:
                self.client.send("code0006:f".encode("utf-8"))

            function_string = args[0]

            try:
                function = self.input_functions[function_string]
            except KeyError:
                self.client.send("code0005:f".encode("utf-8"))
                continue

            response = function(args)
            print(response)

            try:
                self.client.send(response.encode("utf-8"))
            except AttributeError:
                continue

    def signin(self, args):
        """password and username in a list to login"""
    
        if len(args) > 3:
            return "code0000:m"
    
        try:
            userName = args[1]
            password = args[2]
        except IndexError:
            return "code0004:i"
    
        users_on_file = users.loadUsers()
    
        try: 
            passwordOnFile = users_on_file[userName]
        except KeyError:
            return "code0004:u"
    
        if password != passwordOnFile:
            return "code0004:c"
        else:
            self.input_functions.update({
                "new_game": self.new_game
                })
            self.username = userName
            return "code0004:s"

    def new_game(self, args):
        self.game = Game(self.username)
        return "New game created by " + self.username

while True:
    client, addr = server.accept()
    Instance(client)

    
