#201602038 LEE MI JIN
import socket
import struct

s1 = socket.socket(socket.AF_PACKET,socket.SOCK_RAW, socket.htons(0x0800))

slicing_dst = []
slicing_src = []
while True:
	packet = s1.recvfrom(65565)
	packet = packet[0]
	ethernet_header = struct.unpack('!6s6s2s', packet[0:14])
		
	print("=============================================")
	print("		Ethernet II			")
	print("=============================================")
	dst_ethernet_addr = ethernet_header[0].hex()		
	src_ethernet_addr = ethernet_header[1].hex()
	protocol_type = "0x"+ethernet_header[2].hex()

	for i in range(0,6):
		slicing_dst.append(dst_ethernet_addr[(2*i):(2*i)+2])
		slicing_src.append(src_ethernet_addr[(2*i):(2*i)+2])

	print("Destination MAC address : ",slicing_dst[0]+":"+slicing_dst[1]+":"+slicing_dst[2]+":"+slicing_dst[3]+":"+slicing_dst[4]+":"+slicing_dst[5])
	print("Source MAC address : ",slicing_src[0]+":"+slicing_src[1]+":"+slicing_src[2]+":"+slicing_src[3]+":"+slicing_src[4]+":"+slicing_src[5])
	print("protocol : ",protocol_type)
	print("---------------------------------------------")

	if protocol_type == "0x0800" :

		ip_header = struct.unpack('!BBHHHBBH4s4s',packet[14:34])
		print("=============================================")
		print("         IPv4                     ")
		print("=============================================")

		# ip version
		version = ip_header[0] >> 4

		#ip header length
		ip_header_length = (ip_header[0] & 0xF) << 2
		#TOS
		tos = ip_header[1]
		#total length
		total_length = ip_header[2]
		#Identification
		identification = ip_header[3]
		#Flags
		flags = ip_header[4] >> 13
		#Fragment offset
		fragment_offset = (ip_header[4]& 0x1FFFF) << 2
		#TTL
		ttl = ip_header[5]	
		#protocol
		protocol = ip_header[6]
		#header checksum
		hchecksum = ip_header[7]	
		#source ip address
		source_address = socket.inet_ntoa(ip_header[8])
		#destination ip address
		destination_address = socket.inet_ntoa(ip_header[9])
	
		print("Version : ",version)
		print("Internet Header Length : ",ip_header_length)
		print("TOS :",tos)
		print("Total length : ",total_length)
		print("Identification :",identification)
		print("Flags : ",flags)
		print("Fragment offset : ",fragment_offset)
		print("TTL : ",ttl)		
		print("Protocol : ",protocol)
		print("Header Checksum : ",hchecksum)
		print("Source IP address :",source_address)
		print("Destination IP address : ",destination_address)
	
	else :
		print("Protocol is not 0x0800")		


	headers_length = ip_header_length+14
	# case : TCP
	if ip_header[6] == 6 :
		print("=============================================")
		print("		TCP Header			    ")
		print("=============================================")
		tcp_header = struct.unpack("!HHLLBBHHH",packet[headers_length:headers_length+20])
	
		# Source Port
		print("Surce Port : ",tcp_header[0])
		print("Destination Port : ",tcp_header[1])
		print("Sequence Number : ",tcp_header[2])	
		print("Acknowledge Number : ",tcp_header[3])
		# Data offset 4 bits
		print("Data offset : ",tcp_header[4] >> 4 )
		# Reserved 3 bits
		print("Reserved : ",(tcp_header[4] & 0xF) << 2 )
		# NS 1 bits
		print("NS : ")
		# CWR  tcp_header[5] 1 bits
		print("CWR : ")
		# ECE 1 bits
		print("ECE : ")
		# URG 1 bits
		print("URG : ")
		# ACK 1 bits
		print("ACK : ")
		# PSH 1 bits
		print("PSH : ")
		# RST 1 bits
		print("RST : ")
		# SYN 1 bits
		print("SYN : ")
		# FIN 1 bits
		print("FIN : ")
		# Window Size 32 bits
		print("Window Size : ",tcp_header[6])
		# TCP Chcksum 32 bits
		print("TCP Checksum : ",tcp_header[7])
		# Urgent Pointer 32 bits
		print("Urgent Pointer : ",tcp_header[8])

	
	# case : UDP
	if ip_header[6] == 17:
		print("=============================================")
		print("		UDP Header			    ")
		print("=============================================")
		udp_header = struct.unpack("!HHHH",packet[headers_length:headers_length+8])

		print("Source Port : ",udp_header[0])
		print("Destination Port : ",udp_header[1])
		print("UDP Length : ",udp_header[2])
		print("UDP Checksum : ",udp_header[3])


	break
