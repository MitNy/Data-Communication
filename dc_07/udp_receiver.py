import socket
import os

# receiver 요구 사항
# 데이터 수신시 checksum 무결성 검사
# sequence number 확인, ACK은 수신하고자 하는 다음 프레임의 순서 번호를 modular-2 연산으로 계산한 값을 표시

ip_address = '127.0.0.1'
port_number = 2345

receiver_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
receiver_sock.bind((ip_address,port_number))
while True:
	print("------------------------------------------------------")
	print("Receiver socket open...")
	print("Listening...")

	data_size = 0
	data,addr = receiver_sock.recvfrom(1060)

	f = open("./new_file.png","wb")
	f.write(data)
	f.close()
	
	receiver_sock.sendto(data,addr)
