import socket, os, tools, users, threading, json
from game import Game
from time import time
from datetime import datetime
from dataclasses import dataclass, field

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

@dataclass
class InstanaceInfo:
    client: socket.socket
    ip: str = ""
    player_id: str  = ""
    cport: str  = ""
    block_counter: int  = ""
    big_block_counter: int  = ""
    username: str  = "<<NUL>>"
    input_functions: dict  = field(default_factory=dict)
    responses: dict  = field(default_factory=dict)

class Instance:
    def __init__(self, client):
        """client arg here is client var assigned from server.accepet()"""

        # init here to keep some track of vars
        # self.game defined further either at signin, load game
        ii = InstanaceInfo(client)  # for better access across class
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
    

if __name__ == "__main__":
    t = Thread(target=exit)
    t.start()  # classic thrading

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(1)

    print(f"Server listening on {ip}:{port}")
    signup_ip = {}
    blocked_ips = []

    while True:
        client, addr = server.accept()

        if addr[0] in blocked_ips:
            continue

        try:
            client.send("ok".encode("utf-8"))
            client.send("code0006:f\n".encode("utf-8"))
        except e:
            print(e)
            continue

        Instance(client)
