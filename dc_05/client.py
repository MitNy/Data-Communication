# 201602038 이미진
import socket

serverIP = '127.0.0.1'
serverPort = 3333

client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("=============================================================================")
print("*	String Change Progam			")
print("=============================================================================")
print("* Type = 0,1,2,3					")
print("* if Type == 0 : Change all letters to uppercase.")
print("* if Type == 1 : Change all letters to lowercase.")
print("* if Type == 2 : Change upper case to lower case and lower case to upper case.")
print("* if Type == 3 : Change the sentence backwards.")
print("=============================================================================")

while True :
	client_msg = input("Input your Message : ")
	client_sock.sendto(client_msg.encode(), (serverIP, serverPort))
	print("Send Message to Server...")
	print("Received Message from Server : "+((client_sock.recv(1024)).decode()))
	print("---------------------------------------------------------------------------")
