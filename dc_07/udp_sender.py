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
	buffer = []
	sender_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	print("[+] Connected with Receiver")
	print("Receiver IP = ",receiverIP)
	print("Receiver Port = ",receiverPort)
	print("------------------------------------------------------")
	input_file = input("Input file : ")
	padding_name = input_file.ljust(15,)
	data_size = 0	
	with open(input_file,"rb") as f:
		file_size = os.path.getsize("./"+input_file+"")
		print("[+] Sending file...")
		data = f.read(1024)
		sender_sock.sendto(data,(receiverIP,receiverPort))

		f.close()
	print("Send Message to Server...")
	print("------------------------------------------------------")
	sender_sock.close()
