import socket

serverIP = '192.168.44.128'
serverPort = 8000

client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_sock.connect((serverIP,serverPort))
print("Connect to Server ...")

client_msg = input("Input Message : ")
client_sock.send(client_msg.encode())
print("Send Message to Server ...")
print("Received Message from Server :"+(client_sock.recv(1024)).decode("utf-8"))
