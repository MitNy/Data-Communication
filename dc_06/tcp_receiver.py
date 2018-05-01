import socket
import struct
import os

ip_address = "127.0.0.1"
port_number = 2345

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((ip_address, port_number))

while True:
	print("-----------------------------------")
	print("Listening ...")
	server_sock.listen()

	client_sock, addr = server_sock.accept()
	print("[+] Client connected: ", addr)

	file_size = 0
	data_size =0
	while True:
		data = client_sock.recv(1040)
		value = 0
		encode_value = value.to_bytes(1,byteorder="big")
		if data[:1] == encode_value :
			file_name = data[1:11].decode()
			path = "./photo/new_"+file_name.rstrip()+""
			f = open("./photo/new_"+file_name.rstrip()+"","wb")
			file_size = os.path.getsize("./"+file_name.rstrip()+"")
			print("File Name  = ",file_name)
			print("File Size = ",file_size)
			print("File Path = ",path)
			print("-----------------------------------")

		if not data:
			break
		if data[:1] == encode_value :
			f.write(data[16:1040].rstrip())
		else :
			f.write(data[16:1040])
			data_size += len(data[16:1040])

		print(data_size,"/",file_size," , ","{0:.2f}".format((data_size/float(file_size))*100),"%")

	f.close()
	client_sock.close()
	print("[+] File Receive End...")
	print("[-] Client disconnected")
