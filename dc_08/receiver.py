#201602038 이미진
import socket
import os
import hashlib
import time
import struct

# receiver 요구 사항
# 데이터 수신시 checksum 무결성 검사
# sequence number 확인, ACK은 수신하고자 하는 다음 프레임의 순서 번호를 modular-2 연산으로 계산한 값을 표시

ip_address = '127.0.0.1'
port_number = 2345
 
receiver_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
receiver_sock.bind((ip_address,port_number))
 
 
def sha1generator(seqNumber,fileData):
	h = hashlib.sha1()
	h.update(seqNumber+fileData)
	return h.digest()
     
ACK = 0
i = 0
while True:
	print("-----------------------------------")
	print("Listening ...")
     
	data,addr = receiver_sock.recvfrom(1060)
	print("[+] Sender connected: ", addr)
	file_name = data[0:11].decode().rstrip()
	file_size = os.path.getsize("./"+file_name+"")
	path = "./receivedFile/new_"+file_name+""
	checksum = data[15:35]
	sequence_number = data[35:36]
	
	info_checksum = sha1generator(sequence_number,data[36:1060])
	if checksum == info_checksum:
		ACK = 1
		encode_ack = ACK.to_bytes(4, byteorder = "big")
		receiver_sock.sendto(encode_ack, addr)
     
	elif checksum != info_checksum:
		ACK = 2
		print("* Packet corrupted!! *** - Send To Sender NAK(2)")
		encode_ack = ACK.to_bytes(4, byteorder = "big")
		receiver_sock.sendto(encode_ack, addr)
		continue
 
	print("File Name = ",file_name)
	print("File Size = " ,file_size)
	print("File Path = ",path)
	print("-----------------------------------")
	f = open(path, "wb")
	data_size = 0
  
	r = 1
	while True:
		i+=1
		data, addr = receiver_sock.recvfrom(1060)
		checksum = data[15:35]
		sequence_number = data[35:36]
		encode_number = struct.unpack("!B",data[35:36])
		seqNumber = encode_number[0]

		if not data:
			break
         
		if seqNumber != r:
			ACK = seqNumber^1
			encode_ack = ACK.to_bytes(4, byteorder = "big")
			receiver_sock.sendto(encode_ack, addr)
			continue
 
		if sha1generator(sequence_number,data[36:1060]) != checksum:
			print("* Packet corrupted!! *** - Send To Sender NAK(2)")
			ACK = 2
			encode_ack = ACK.to_bytes(4, byteorder = "big")
			receiver_sock.sendto(encode_ack, addr)
			continue
 
		if i == 3:
			print("*** Intentional delay ***")
			time.sleep(5)
			ACK = 3
			continue           
      
		f.write(data[36:1060])
		data_size += len(data[36:1060])
         
		ACK = seqNumber^1
		encode_ack = ACK.to_bytes(4, byteorder = "big")
		receiver_sock.sendto(encode_ack, addr)

		print(data_size,"/",file_size," , ","{0:.2f}".format((data_size/float(file_size))*100),"%")
		r = r^1
 
		if data_size == file_size:
			break
 
	f.close()
	print("[+] File Receive End...")
	print("[-] Sender disconnected")
