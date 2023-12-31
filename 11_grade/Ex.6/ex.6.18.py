from scapy.layers.inet import *
from scapy.all import *

syn_segment = TCP(sport=2000, dport=80, seq=123, flags='S') # 24601
syn_packet = IP(src="172.16.17.136", dst='www.google.com')/syn_segment

# send(syn_packet, iface="Wi-Fi")

syn_ack_packet = sr1(syn_packet, iface="Wi-Fi")/syn_segment
print("syn ack packet")
syn_ack_packet.show()


ack_segment = ""
ack_packet = IP(dst='www.google.com')/ack_segment
print("ack packet")
ack_packet.show()
send(ack_packet)
print("packet sent")
