#201602038 이미진
import socket
import os
import hashlib
import struct
import time

# sender 요구사항
# window size 4
# ack 수신
 
receiverIP = '127.0.0.1'
receiverPort = 2345

def seqNumAck(sequence_number,ACK):
	sequence_number = sequence_number << 4
	ACK = ACK & 0b1111
	return (sequence_number|ACK).to_bytes(1,"big")
 
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
         
		encode_seqAck = seqNumAck(sequence_number,ACK)
		info_checksum = sha1generator(encode_seqAck,"".encode().ljust(1024,))
            
		sender_sock.sendto((padding_name.encode()+padding_size.encode()+info_checksum+encode_seqAck).ljust(1060,),(receiverIP,receiverPort))
             
		encode_seqAck = sender_sock.recv(1)
		seqAck = encode_seqAck[0]
		
		buf = [0]*4
		tmp = []
		i = 0
		s = 0
		window_size = 4
		received_ack = 0
		data = f.read(1024)     
		while data:
			while s < window_size:
				data_size += len(data)
		
				if not data:
					break

				buf[i] = data
				tmp.extend([i])
				encode_seqAck = seqNumAck(sequence_number,ACK)
				checksum = sha1generator(encode_seqAck,data)

				sender_sock.sendto(padding_name.encode()+padding_size.encode()+checksum+encode_seqAck+data,(receiverIP,receiverPort))
				print(data_size,"/",file_size," , ","{0:.2f}".format((data_size/float(file_size))*100),"%")

				i = (i+1)%len(buf)
				sequence_number = (ACK+1)%len(buf)
				ACK = (ACK+1)%len(buf)

				data = f.read(1024)
				s += 1
	
			try:
				sender_sock.settimeout(1)
				received_encode_seqAck = sender_sock.recv(1)
				received_ack = received_encode_seqAck[0] & 0b1111
				tmp_index = tmp.index(received_ack)

				for j in range(tmp_index):
					del tmp[0]
					s -= 1
				continue

			except:
				print("** Time Out **")
				ACK = 3
				continue

			if len(tmp) == 0:
				break
			if data_size == file_size:
				break
             
		f.close()
		sender_sock.close()
		print("-----------------------------------")

