import scapy
from scapy.sendrecv import *

packets = sniff(10, iface='\\device\\NPF_Loopback')
packets.show()
