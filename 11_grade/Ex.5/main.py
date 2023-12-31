from scapy.all import *
from scapy.layers.dns import DNSQR, DNS, IP

print("a")
def print_query_name(dns_packet):
    print(dns_packet[DNSQR].qname)


def filter_dns(packet):
    return DNS in packet and packet[DNS].opcode == 0 and packet[DNSQR].qtype == 1

print("a")
my_packet = IP(dst="www.google.com")
my_packet.show()
print("a")

#sniff(count=10, lfilter=filter_dns, prn=print_query_name)
