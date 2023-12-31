from scapy.layers.inet import *
from scapy.all import *
import time
L = []
for i in range(79, 1024):
    print(i)
    syn_segment = TCP(sport=2000, dport=i, seq=123, flags='S')

    syn_packet = IP(dst='www.google.com') / syn_segment
    # send(syn_packet, iface="Wi-Fi")

    syn_ack_packet = sr1(syn_packet, iface="Wi-Fi", timeout=1)
    try:
        syn_ack_packet.show()
        print(i)
        L.append(i)
    except AttributeError:
        pass

    ack_segment = ""
    ack_packet = IP(dst='www.google.com') / ack_segment
    send(ack_packet)
    print("packet sent")
print(L)
