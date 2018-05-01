import socket
import struct

ip_address = "127.0.0.1"
port_number = 2345

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((ip_address, port_number))

while True:
	print("--------------------------")
	print("Listening ...")
	server_sock.listen()

	client_sock, addr = server_sock.accept()
	print("[+] Client connected: ", addr)

	total_size = 0
	while True:
		data = client_sock.recv(1040)

		data_size = 0
		value = 0
		encode_value = value.to_bytes(1,byteorder="big")
		if data[:1] == encode_value:
			file_name = data[1:11].decode()
			f = open("./photo/new_"+file_name.rstrip()+"","wb")

		if not data:
			break
		if data[:1] == encode_value :
			total_size += len(data[16:1040].rstrip())/1024
			data_size = len(data[16:1040].rstrip())/1024
			f.write(data[16:1040].rstrip())
		else :
			total_size += len(data[16:1040])/1024
			data_size = len(data[16:1040])/1024
			f.write(data[16:1040])

	file_size = int(total_size*1024)

	print(file_size)
	f.close()
	print("[+] Download complete!")

	client_sock.close()
	print("[-] Client disconnected")
