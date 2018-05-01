import socket
import os

serverIP = "127.0.0.1"
serverPort = 2345

while True:
	client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	client_sock.connect((serverIP,serverPort))
	print("[+] Connected with Server")
	f_send = input("Input file name : ")
	with open(f_send, "rb") as f:
		file_size = os.path.getsize("./"+f_send+"")
		kb_size = file_size/1024
		name_padding = f_send.ljust(11,);
		size_padding = str(int(kb_size)).rjust(4,);
		print("[+] Sending file...")
		data = f.read(1024)
		msg_type = 0
		data_size = 0
		while(data):
			data_size += len(data)
			print(data_size,"/",file_size," , ","{0:.2f}".format((data_size/float(file_size))*100),"%")
			encode_type = msg_type.to_bytes(1,byteorder="big")
			if msg_type == 0:
				client_sock.send((encode_type+name_padding.encode()+size_padding.encode()).ljust(1040,))
			msg_type = 1
			encode_type = msg_type.to_bytes(1,byteorder="big")
			if msg_type == 1:
				client_sock.send(encode_type+name_padding.encode()+size_padding.encode()+data)
				data = f.read(1024)
		f.close()

	client_sock.close()
	print("[-] Disconnected")
