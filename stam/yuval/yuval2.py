import threading
import time
import random
from scapy.all import *
from scapy.layers.inet import TCP, IP

server_ip = "127.0.0.1"


class Server:
    def _init_(self):
        self.seq_number = 101
        self.ack_number = 0

    def filter_syn_packet(self, packet):
        if IP in packet:
            return TCP in packet and packet.seq == 100 and packet[TCP].flags == "S"
        return False

    def filter_ack_packet(self, packet):
        return IP in packet and TCP in packet and packet.seq == 101 and packet[TCP].flags == "A"

    def create_syn_ack_packet(self):
        try:
            return IP(dst=server_ip) / TCP(sport=80, dport=random.randrange(1025, 65536), flags='SA')
        except TypeError:
            return None

    @staticmethod
    def split_message(num, msg):
        if num > len(msg):
            print('ERROR!')
            exit(1)
        lst = []
        index_lst = [0]
        indexer = 0
        while len(msg) != 0:
            if num == 1:
                lst.append(msg)
                msg = ""
            else:
                x = random.randrange(1, len(msg) - num + 1)
                indexer += x
                num -= 1
                new_msg = msg[0:x]
                msg = msg[x:]
                index_lst.append(indexer)
                lst.append(new_msg)
        return lst, index_lst

    def create_packet(self):
        try:
            return IP(dst=server_ip) / TCP(sport=80, dport=random.randrange(1025, 65536))
        except TypeError:
            return None

    def send_packet(self, packet):
        packet[TCP].seq = self.seq_number
        packet[TCP].ack = self.ack_number
        if Raw in packet:
            self.seq_number += len(packet[Raw])
        self.seq_number += 1
        send(packet, iface='\\device\\NPF_Loopback')

    def handle_packet(self, packet):
        if self.filter_syn_packet(packet):
            self.send_packet(self.create_syn_ack_packet())
        if self.filter_ack_packet(packet):
            packet.show()


def server():
    server_obj = Server()
    sniff(prn=server_obj.handle_packet, iface='\\device\\NPF_Loopback')


if __name__ == "__main__":
    server()