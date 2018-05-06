import socket
import os
import sys

# sender 요구 사항
# checksum 20 byte / sequence number 1 byte / data 1024 byte
# sequence number : 프레임 순서 보장, 0-1
# checksum : 프레임 무결성 보장, sequence number+file data sha1 encode

serverIP = '127.0.0.1'
serverPort = 2345

while True:
	client_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	input_file = input("Input file : ")
	client_sock.sendto(input_file.encode(),(serverIP,serverPort))
	print("Send Message to Server...")
	print("Received Message from Server : "+((client_sock.recv(1024)).decode()))
	print("------------------------------------------------------")
	client_sock.close()
