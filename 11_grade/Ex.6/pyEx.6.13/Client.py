import threading
from scapy.layers.dns import *
from scapy.sendrecv import *
import socket

send_msg = True

"""

░█████╗░██╗░░░░░██╗███████╗███╗░░██╗████████╗       ░░███╗░░
██╔══██╗██║░░░░░██║██╔════╝████╗░██║╚══██╔══╝       ░████║░░
██║░░╚═╝██║░░░░░██║█████╗░░██╔██╗██║░░░██║░░░       ██╔██║░░
██║░░██╗██║░░░░░██║██╔══╝░░██║╚████║░░░██║░░░       ╚═╝██║░░
╚█████╔╝███████╗██║███████╗██║░╚███║░░░██║░░░       ███████╗
░╚════╝░╚══════╝╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░       ╚══════╝"""


class Client:
    def __init__(self):
        self.my_socket = socket.socket()

    @staticmethod
    def send_message():
        while True:
            try:
                ip = input("enter your server ip: ")
                socket.inet_pton(socket.AF_INET, ip)
                break
            except socket.error:
                pass
        message = input("enter a message: ")
        for i in message:
            letter = ord(i) + 2000
            packet = IP(dst=ip) / UDP(dport=letter, sport=2000, len=0)
            send(packet, iface="\\device\\NPF_Loopback", verbose=False)
            # send(packet, iface="Wi-Fi")

        packet = IP(dst=ip) / UDP(dport=2127, sport=2000, len=0)
        send(packet, iface="\\device\\NPF_Loopback", verbose=False)


class Server:

    def __init__(self):
        self.server_socket = socket.socket()
        self.client_sock = None

    @staticmethod
    def lfilter(packet):
        return IP in packet and UDP in packet and packet[UDP].len == 0

    @staticmethod
    def execute(packet):
        global send_msg
        charInString = packet[UDP].dport
        if charInString == 2000 and not send_msg:
            send_msg = True
            print()
        elif not send_msg:
            print(chr(charInString - 2000), end='')


def main_client():
    Client_sock = Client()
    Client_sock.send_message()


def main_sever():
    Server_sock = Server()
    # packet = sniff(lfilter=lfilter, prn=execute)
    sniff(lfilter=Server_sock.lfilter, iface='\\device\\NPF_Loopback', prn=Server_sock.execute)


if __name__ == "__main__":
    t = threading.Thread(target=main_sever, daemon=True)
    t.start()
    while True:
        if send_msg:
            main_client()
            time.sleep(1)
            send_msg = False
        time.sleep(0.5)
