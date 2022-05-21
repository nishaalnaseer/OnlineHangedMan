import socket

ip, port = "172.104.181.124", 65000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

while True:
    msg = input("send to server: ")
    client.send(msg.encode("utf-8"))

    msg = client.recv(1024).decode("utf-8")
    print(msg)