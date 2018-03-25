#201602038 LEE MI JIN
import socket
import struct

s1 = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0800))
#s2 = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

slicing_dst = []
slicing_src = []
while True:
	packet = s1.recvfrom(4096)

	ethernet_header = struct.unpack('!6s6s2s', packet[0][0:14])
	
	
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

	packet1 = s1.recvfrom(65565)
	packet1 = packet[0]
	ip_header = struct.unpack('!BBHHHBBH4s4s',packet1[14:34])
	print("=============================================")
	print("         IPv4                     ")
	print("=============================================")
	# ip version
	ip_version = ip_header[0]
	version = ip_version >> 4

	#ip header length
	ip_length = ip_version & 0xF
	ip_header_length = ip_length * 4

	#TOS
	tos = ip_header[1]

	#total length
	total_length = ip_header[2]

	#Identification
	identification = ip_header[3]
	#Flags
	flags = ip_header[4] >> 13
	#Fragment offset
	fragment_offset = (ip_header[4]&0x1FFFF) << 2

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
	
	
	break
