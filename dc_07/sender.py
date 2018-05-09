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

def sha1generator(seqNumber,fileData):
	encode_number = seqNumber.to_bytes(1,byteorder="big")
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
		data_size = 0

		print("[+] Sending file...")
		# file info transfer
		info_checksum = sha1generator(sequence_number,"".encode().ljust(1024,))
		encode_seqNumber = sequence_number.to_bytes(1,byteorder="big")
		
		sender_sock.sendto((padding_name.encode()+padding_size.encode()+info_checksum+encode_seqNumber).ljust(1060,),(receiverIP,receiverPort))

		ACK = struct.unpack("!1i",sender_sock.recv(4))[0]
		sequence_number = ACK
		if ACK == 1:
			data = f.read(1024)
			while data:
				data_size += len(data)
				sequence_number = data[36]
				encode_number = sequence_number.to_bytes(1,byteorder="big")
				checksum = sha1generator(sequence_number,data)
				sender_sock.sendto(padding_name.encode()+padding_size.encode()+checksum+encode_number+data,(receiverIP,receiverPort))
				
				data = f.read(1024)
				print(data_size,"/",file_size," , ","{0:.2f}".format((data_size/float(file_size))*100),"%")
				try:
					sender_sock.settimeout(1)
					ACK = sender_sock.recv(4)
					sequence_number = struct.unpack("!1i",sender_sock.recv(4))[0]
				except:
					ACK = 0
					continue

				if data_size == file_size:
					break								
	f.close()
	sender_sock.close()
	print("-----------------------------------")
