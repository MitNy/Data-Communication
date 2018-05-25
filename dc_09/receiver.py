#201602038 이미진
import socket
import os
import hashlib
import time
import struct

# receiver 요구사항
# sliding window 크기 1
# checkusm 체크

ip_address = '127.0.0.1'
port_number = 2345
 
receiver_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
receiver_sock.bind((ip_address,port_number))
 

def seqNumAck(received_seqAck,ACK):
	ACK = received_seqAck & 0b1111
	received_seqAck = received_seqAck << 4
	return (received_seqAck|ACK).to_bytes(1,"big")

def sha1generator(seqAck,fileData):
	h = hashlib.sha1()
	h.update(seqAck+fileData)
	return h.digest()

while True:
	print("-----------------------------------")
	print("Listening ...")

	ACK = 0  
	data,addr = receiver_sock.recvfrom(1060)
	print("[+] Sender connected: ", addr)
	file_name = data[0:11].decode().rstrip()
	file_size = os.path.getsize("./"+file_name+"")
	path = "./receivedFile/new_"+file_name+""
	checksum = data[15:35]
	received_seqAck = data[35:36]
	decode_seqAck = struct.unpack("!B",received_seqAck)
	seqAck = decode_seqAck[0]
	
	info_checksum = sha1generator(received_seqAck,data[36:1060])
	
	if checksum == info_checksum:
		received_seqAck = seqAck >> 4
		encode_seqAck = seqNumAck(received_seqAck,ACK)
		receiver_sock.sendto(encode_seqAck,addr)
	else:
		print("** Checksum Error **")
 
	print("File Name = ",file_name)
	print("File Size = " ,file_size)
	print("File Path = ",path)
	print("-----------------------------------")
	f = open(path, "wb")
	data_size = 0
	
	while True:
		data, addr = receiver_sock.recvfrom(1060)
		checksum = data[15:35]
		seqAck = data[35:36]
		decode_seqAck = struct.unpack("!B",seqAck)

		if not data:
			break
 
		if sha1generator(seqAck,data[36:1060]) != checksum:
			print("** Checksum Error **")
			break 
      
		f.write(data[36:1060])
		data_size += len(data[36:1060])
		print(data_size,"/",file_size," , ","{0:.2f}".format((data_size/float(file_size))*100),"%")

		received_seqAck = decode_seqAck[0] >> 4
		encode_seqAck = seqNumAck(received_seqAck,ACK)

		receiver_sock.sendto(encode_seqAck,addr)
		if data_size == file_size:
			break
 
	f.close()
	print("[+] File Receive End...")
	print("[-] Sender disconnected")
