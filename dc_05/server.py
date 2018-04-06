# 201602038 이미진
import socket

ip_address = '127.0.0.1'
port_number = 3333

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")
print("---------------------------------------------------------------------------")
while True :
	print("Listening...")
	data,addr = server_sock.recvfrom(5000)
	de_msg = data.decode()
	type_check = de_msg[0]
	convert_msg=""
	print("Type of Message : "+type_check)
	print("Received Message from client : "+de_msg[1:])
	
	if "0" <= type_check <= "3" :
		if type_check == "0":
			convert_msg = de_msg[1:].upper()
			print("Converted Message : "+convert_msg)
			server_sock.sendto(convert_msg.encode(), addr)
			print("Send to Client Converted Message .....")
		if type_check == "1":
			convert_msg = de_msg[1:].lower()
			print("Converted Message : "+convert_msg)
			server_sock.sendto(convert_msg.encode(), addr)
			print("Send to Client Converted Message .....")
		if type_check == "2":
			convert_msg = de_msg[1:].swapcase()
			print("Converted Message : "+convert_msg)
			server_sock.sendto(convert_msg.encode(), addr)
			print("Send to Client Converted Message .....")
		if type_check == "3":
			convert_msg = ''.join(reversed(de_msg[1:]))
			print("Converted Message : "+convert_msg)
			server_sock.sendto(convert_msg.encode(), addr)
			print("Send to Client Converted Message .....")
	else :
		error_msg = "Type does not exist. So, server can't send to message."
		server_sock.sendto(error_msg.encode(),addr)
		print("Type does not exist. Can't send to client.")


	print("---------------------------------------------------------------------------")
