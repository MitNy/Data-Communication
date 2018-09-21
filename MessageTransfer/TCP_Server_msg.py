import socket
import struct

ip_address = '192.168.44.128'
port = 8000

server_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_sock.bind((ip_address,port))

while True:
	print("--------------------------")
	print("Listening...")
	server_sock.listen()

	client_sock,addr = server_sock.accept()
	print("[+] Client connected : ",addr)
	data = client_sock.recv(5000)
	print("Received Message from client : "+data.decode())
	client_sock.send(data)
	print("Send Message back to client")
