import threading
import time
import random
from scapy.all import *
from scapy.layers.inet import TCP, IP

server_ip = "127.0.0.1"


class Client:
    def _init_(self):
        self.seq_number = 100
        self.ack_number = 0

    def filter_syn_ack_packet(self, packet):
        if packet is not None:
            if TCP in packet:
                return packet[TCP].flags == "SA" and packet[TCP].seq == 101

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

    def add_seq_num(self, packet):
        packet[TCP].seq = self.seq_number
        if Raw in packet:
            self.seq_number += len(packet[Raw])
        self.seq_number += 1

    def send_packet(self, packet):
        send(packet, iface='\\device\\NPF_Loopback')

    def create_packet(self, lst, i):
        try:
            packet = IP(dst=server_ip) / TCP(sport=80, dport=random.randrange(1025, 65536)) / Raw(load=lst[i])
            self.add_seq_num(packet)
            return packet
        except TypeError:
            return None

    def create_syn_packet(self):
        try:
            packet = IP(dst=server_ip) / TCP(sport=80, dport=random.randrange(1025, 65536), flags='S')
            self.ack_number = random.randint(1, 1000)
            packet[TCP].ack = self.ack_number
            self.add_seq_num(packet)
            return packet
        except TypeError:
            return None

    def create_ack_packet(self):
        try:
            packet = IP(dst=server_ip) / TCP(sport=80, dport=random.randrange(1025, 65536), flags='A')
            packet[TCP].ack = self.ack_number
            return packet
        except TypeError:
            return None

    def handle_packet(self, packet):
        if self.filter_syn_ack_packet(packet):
            self.ack_number = packet[TCP].seq
            self.send_packet(self.create_ack_packet())
        else:
            msg = input()
            lst_msg, smt = self.split_message(int(len(msg) / 4), msg)
            for i in range(len(lst_msg)):
                k = random.randrange(0, len(lst_msg))
                self.send_packet(self.create_packet(lst_msg, k))


def client():
    client_obj = Client()
    client_obj.send_packet(client_obj.create_syn_packet())
    sniff(prn=client_obj.handle_packet, iface='\\device\\NPF_Loopback')


if __name__ == "__main__":
    client()
