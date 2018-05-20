#201602038 이미진
import socket
import os
import hashlib
import struct
import time

# sender 요구 사항
# checksum 20 byte / sequence number 1 byte / data 1024 byte
# sequence number : 프레임 순서 보장, 0-1
# checksum : 프레임 무결성 보장, sequence number+file data sha1 encode
# sender는 패킷을 전송할 때마다 타이머를 구동하고 타이머가 만료되기 전에 확인 응답이 도착하면 타이머는 정지되고 다음 패킷을 보낸다.
# 데이터통신 교과서 참고
 
receiverIP = '127.0.0.1'
receiverPort = 2345
 
def sha1generator(sequence_numberber,fileData):
	encode_number = sequence_numberber.to_bytes(1,byteorder="big")
	h = hashlib.sha1()
	h.update(encode_number+fileData)
	return h.digest()
 
i=0
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
		data_size = 0
		print("[+] Sending file...")
         
		while True:
			info_checksum = sha1generator(sequence_number,"".encode().ljust(1024,))
			encode_sequence_numberber = sequence_number.to_bytes(1,byteorder="big")
            
			sender_sock.sendto((padding_name.encode()+padding_size.encode()+info_checksum+encode_sequence_numberber).ljust(1060,),(receiverIP,receiverPort))
             
			try:
				sender_sock.settimeout(4)
				received_ack = sender_sock.recv(4)
				ACK = struct.unpack("!1i", received_ack)[0]
                 
				if ACK == 2:
					continue
				sequence_number = ACK
			except:
				ACK = 3
				continue
             
			if ACK == 1:
				break
			sequence_number = ACK
		data = f.read(1024)
		n = 1     
		while data:
			i += 1
			if ACK == n:
				n = n^1
				data_size += len(data)
				encode_number = sequence_number.to_bytes(1,byteorder="big")
				checksum = sha1generator(sequence_number,data)
				if i == 5:
					checksum = sha1generator(sequence_number,data[20:30])
				sender_sock.sendto(padding_name.encode()+padding_size.encode()+checksum+encode_number+data,(receiverIP,receiverPort))
                 
				try:
					sender_sock.settimeout(4)
					received_ack = sender_sock.recv(4)
					ACK = struct.unpack("!1i", received_ack)[0]
                 
					if ACK == 2 or ACK == 3:
						continue
             
					sequence_number = ACK
				except:
					ACK = 3
					continue
 
				print(data_size,"/",file_size," , ","{0:.2f}".format((data_size/float(file_size))*100),"%")

			elif ACK == 2:
				encode_number = sequence_number.to_bytes(1,byteorder="big")
				checksum = sha1generator(sequence_number,data)
				sender_sock.sendto(padding_name.encode()+padding_size.encode()+checksum+encode_number+data,(receiverIP,receiverPort))
                
				print("* Received NAK - Retransmit!")
				print("Retransmission : ",data_size,"/",file_size," , ","{0:.2f}".format((data_size/float(file_size))*100),"%")
				try:
					sender_sock.settimeout(4)
					received_ack = sender_sock.recv(4)
					ACK = struct.unpack("!1i", received_ack)[0]
					if ACK == 2 or ACK == 3:
						continue
					sequence_number = ACK
				except:
					ACK = 3
					continue
			elif ACK == 3:
				encode_number = sequence_number.to_bytes(1,byteorder="big")
				checksum = sha1generator(sequence_number,data)
				sender_sock.sendto(padding_name.encode()+padding_size.encode()+checksum+encode_number+data,(receiverIP,receiverPort))

				print("* TimeOut!! ***")
				print("Retransmission : ",data_size,"/",file_size," , ","{0:.2f}".format((data_size/float(file_size))*100),"%")
				try:
					sender_sock.settimeout(4)
					received_ack = sender_sock.recv(4)
					ACK = struct.unpack("!1i", received_ack)[0]
					if ACK == 2 or ACK == 3:
						continue
					sequence_number = ACK
				except:
					ACK = 3
					continue
			else :
				try:
					sender_sock.settimeout(4)
					received_ack = sender_sock.recv(4)
					ACK = struct.unpack("!1i", received_ack)[0]
					if ACK == 2 or ACK == 3:
						continue
					sequence_number = ACK
				except:
					ACK = 3
					continue
 
			data = f.read(1024)
             
			if data_size == file_size:
				break
 
		f.close()
		sender_sock.close()
		print("-----------------------------------")

