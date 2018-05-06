import socket
import os
import sys

# sender 요구 사항
# checksum 20 byte / sequence number 1 byte / data 1024 byte
# sequence number : 프레임 순서 보장, 0-1
# checksum : 프레임 무결성 보장, sequence number+file data sha1 encode

receiverIP = '127.0.0.1'
receiverPort = 2345

while True:
	sender_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	print("------------------------------------------------------")
	print("[+] Connected with Receiver")
	print("Receiver IP = ",receiverIP)
	print("Receiver Port = ",receiverPort)
	print("------------------------------------------------------")
	input_file = input("Input file : ")
	padding_name = input_file.ljust(15,)
		
	sender_sock.sendto(input_file.encode(),(receiverIP,receiverPort))
	print("Send Message to Server...")
	print("Received Message from Server : "+((sender_sock.recv(1024)).decode()))
	print("------------------------------------------------------")
	sender_sock.close()
