import socket
SERVER = '127.0.0.1'
PORT = 64001

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((SERVER,PORT))

while True:
    in_data = client.recv(1024)
    print("From server :", in_data.decode())
    out_data = input()
    client.send( bytes( out_data, 'UTF-8'))
    if in_data.decode().upper() == "BYE":
        break


