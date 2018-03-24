#201602038 LEE MI JIN
import socket
import struct

socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
slicing_dst = []
slicing_src = []
while True:
	packet = socket.recvfrom(4096)

	ethernet_header = struct.unpack('!6s6s2s', packet[0][0:14])
	print(ethernet_header)

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
	
	break
