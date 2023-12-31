from scapy import *
from scapy.sendrecv import *
from scapy.layers.inet import *

Ip = "127.0.0.1"


class Server:
    def __init__(self):
        pass

    @staticmethod
    def lfilter_Syn(packet):
        if IP in packet:
            return TCP in packet and packet.seq == 100 and packet[TCP].flags == "S"
        return False

    @staticmethod
    def filter_Ack(packet):
        return IP in packet and TCP in packet and packet.seq == 101 and packet[TCP].flags == "A"


Server_sock = Server()
client_syn_pck = sniff(count=1, lfilter=Server_sock.lfilter_Syn, iface='\\device\\NPF_Loopback')
client_syn_pck.show()

syn_ack_segment = TCP(sport=2345, dport=80, seq=101, flags='SA')
syn_ack_packet = IP(src="127.0.0.1", dst='127.0.0.1')/syn_ack_segment
send(syn_ack_packet)
