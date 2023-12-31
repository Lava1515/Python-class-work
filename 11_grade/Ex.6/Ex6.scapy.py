from scapy.layers.dns import *
from scapy.layers.inet import *

# www.facebook.com
name = input("Enter the url name")
dns_packet = IP(dst='8.8.8.8')/UDP(dport=53)/DNS(qdcount=1, rd=1, qd=DNSQR(qname=name))
x = sr1(dns_packet, iface="Wi-Fi")
count = x[DNS].ancount
for i in range(count):
    data = x[DNS].an[DNSRR][i]
    if data.type == 1:
        print(data.rdata)
        break

