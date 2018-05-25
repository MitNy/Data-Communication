#201602038 이미진
import socket
import os
import hashlib
import struct
import time
 
receiverIP = '127.0.0.1'
receiverPort = 2345
 
def sha1generator(sequence_numberber,fileData):
	encode_number = sequence_numberber
	h = hashlib.sha1()
	h.update(encode_number+fileData)
	return h.digest()

while True: 
	sender_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	print("[+] Connected with Receiver")
	print("Receiver IP = ",receiverIP)
	print("Receiver Port = ",receiverPort)
	print("-----------------------------------")
	input_file = input("Input file : ")
	padding_name = input_file.ljust(11,)
 
	with open(input_file,"rb") as f:
		file_size = os.path.getsize("./"+input_file+"")
		kb_size = file_size/1024
		padding_size = str(int(kb_size)).rjust(4,);
		sequence_number = 0
		ACK = 0
		data_size = 0
		print("[+] Sending file...")
         
		sequence_number = sequence_number << 4
		ACK = ACK & 0b1111
		encode_seqAck = (sequence_number|ACK).to_bytes(1,"big")	
		info_checksum = sha1generator(encode_seqAck,"".encode().ljust(1024,))
            
		sender_sock.sendto((padding_name.encode()+padding_size.encode()+info_checksum+encode_seqAck).ljust(1060,),(receiverIP,receiverPort))
             
		encode_seqAck = sender_sock.recv(1)
		seqAck = encode_seqAck[0]
		ACK = seqAck & 0b00001111

		ACK = 0
		sequence_number = 0

		mem = [None]*8
		tmp = []
		i = 0
		s = 0
		received_ack = 0
		window_size = 4
		
		data = f.read(1024)     
		while data:
			while s < window_size:
				data_size += len(data)
		
				if not data:
					break

				mem[i] = data
				tmp.append(i)

				sequence_number = sequence_number << 4
				ACK = ACK & 0b1111
				encode_seqAck = (sequence_number|ACK).to_bytes(1,"big")

				checksum = sha1generator(encode_seqAck,data)

				sender_sock.sendto(padding_name.encode()+padding_size.encode()+checksum+encode_seqAck+data,(receiverIP,receiverPort))
				print(data_size,"/",file_size," , ","{0:.2f}".format((data_size/float(file_size))*100),"%")

				i = (i+1)%8
				sequence_number = (ACK+1)%8
				ACK = sequence_number
				s = s+1

				data = f.read(1024)

			if len(tmp) == 0:
				break
	
			try:
				sender_sock.settimeout(1)
				received_encode_seqAck = sender_sock.recv(1)
				received_seqAck = received_encode_seqAck[0]
				received_ack = received_seqAck & 0b1111
				tmp_index = tmp.index(received_ack)

				for j in range(tmp_index+1):
					tmp.pop(0)
					s = s-1
				continue

			except:
				print("** Time Out **")
				ACK = 3
				continue

			if data_size == file_size:
				break
             
		f.close()
		sender_sock.close()
		print("-----------------------------------")

