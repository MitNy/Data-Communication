#201602038 이미진
import socket
import os
import hashlib
import time
import struct

ip_address = "127.0.0.1"
port_number = 2345

receiver_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
receiver_sock.bind((ip_address,port_number))

def sha1generator(seqNumber,fileData):
	
	h = hashlib.sha1()
	h.update(seqNumber+fileData)
	return h.digest()

while True:
	ACK = 0

	data,addr = receiver_sock.recvfrom(1060)
	file_name = data[0:11].decode().rstrip()
	file_size = os.path.getsize("./"+file_name+"")
	path = "./receivedFile/new_"+file_name+""
	checksum = data[15:35]
	sequence_number = data[35:36]
	info_checksum = sha1generator(sequence_number,data[36:1060])

	if checksum == info_checksum:
		ACK = 1
		b_ACK = ACK.to_bytes(4, byteorder = "big")
		receiver_sock.sendto(b_ACK, addr)

	print("File Name = ",file_name)
	print("File Size = " ,file_size)
	print("File Path = ",path)
	print("------------------------------------------------------")

	f = open(path, "wb")
	data_size = 0
	while True:
		data, addr = receiver_sock.recvfrom(1060)
		checksum = data[15:35]
		sequence_number = data[35:36]
		file_data = data[36:1060]
		if sha1generator(sequence_number,data[36:1060]) != checksum:
			break

		f.write(data[36:1060])
		data_size += len(file_data)
		print(data_size,"/",file_size," , ","{0:.2f}".format((data_size/float(file_size))*100),"%")	
		if sequence_number == 0:
			ACK = 1
		elif sequence_number == 1:
			ACK = 0
		b_ACK = ACK.to_bytes(4, byteorder = "big")
		receiver_sock.sendto(b_ACK, addr)
		if int(data_size) >= int(file_size):
			print("receive success")	
			break

	f.close()
