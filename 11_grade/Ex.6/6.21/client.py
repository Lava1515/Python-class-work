from scapy import *
from scapy.sendrecv import *
from scapy.layers.inet import *


class client:
    def __init__(self):
        pass

    @staticmethod
    def filter_Syn_Ack(packet):
        if IP in packet:
            return TCP in packet and packet[TCP].seq == 101 and packet[TCP].flags == "SA"
        return False


Client = client()
syn_segment = TCP(sport=2345, dport=80, seq=100, flags='S')

syn_packet = IP(src="127.0.0.1", dst='127.0.0.1')/syn_segment

syn_ack_packet = sr1(syn_packet, iface='\\device\\NPF_Loopback')

'''syn_ack_packet = sniff(count=1, lfilter=Client.filter_Syn_Ack, iface='\\device\\NPF_Loopback')'''
syn_ack_packet.show()


