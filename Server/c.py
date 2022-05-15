import socket, tools, os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip, port = "127.0.0.1", 65000
client.connect((ip, port))

while True:
    inp = input("Send to server: ")
    if inp == exit:
        os._exit(0)

    client.send(inp.encode("utf-8"))

    response = client.recv(1024).decode("utf-8")
    print(response)