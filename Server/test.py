import socket, os, tools, users, threading, json
from game import Game
from time import time
from datetime import datetime
from dataclasses import dataclass

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
    ip: str
    player_id: str
    cport: str
    block_counter: int
    big_block_counter: int
    username: str
    input_functions: dict
    responses: dict
    client: socket.socket

ii = InstanaceInfo(ip=ip)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 65000))
server.listen(1)
print(type("helo"))

while True:
    client, addr = server.accept()
    print(type(client))
    print(type("helo"))
print(ii)