import multiprocessing
import hashlib
import socket
import time

from protocol import Protocol
import json


class Client:
    def __init__(self):
        # self.processes_num = max(multiprocessing.cpu_count() - 5, 1)
        self.processes_num = 7
        self.socket = Protocol()
        self.chunks = None
        self.start_ = 0
        self.end_ = 0
        self.send_list = []
        self.pros_list: list[multiprocessing.Process] = []
        self.found = False

    def connect(self, ip, port):
        self.socket.connect((ip, port))

    def disconnect(self):
        self.socket.close()
        print("The client have been disconnected")

    def get_work(self):
        self.socket.send_msg("get work man".encode())
        work = json.loads(self.socket.get_msg().decode())
        self.set_selfs(work)

    def set_selfs(self, work):
        print("in work", work)
        self.start_ += int(work["range_max"]) - int(work["chunk"])
        print("start", self.start_)
        self.end_ += int(work["range_max"]) - 1
        print("end", self.end_)
        self.chunks = int(work["chunk"]) // self.processes_num
        print("chunks", self.chunks)

    def split_pros(self):
        lst = []
        for i in range(self.processes_num):
            p = multiprocessing.Process(target=self.md_5, args=(self.socket, self.chunks * i + self.start_, self.chunks * (i + 1) - 1
                                                                + self.start_), daemon=True)
            p.start()
            lst.append(p)
        self.pros_list = lst

    @staticmethod
    def md_5(sock, start, end):
        target_hash = "EC9C0F7EDCC18A98B1F31853B1813301"
        count = 0
        while start != end:
            hash_attempt = hashlib.md5(str(start).zfill(10).encode()).hexdigest()
            if hash_attempt.upper() == target_hash:
                name = {multiprocessing.current_process().name}
                print(f"Process {name} found the original input: {start}")
                sock.send_msg(f"WE FOUND THE NUMER ITS {start} and found in {name}".encode())
                break

            start += 1
            count += 1
            if count == 500000:
                sock.send_msg((json.dumps({"count": count}).encode()))
                count = 0
        sock.send_msg((json.dumps({"count": count}).encode()))


def main():
    my_client = Client()
    my_client.connect('127.0.0.1', 8820)
    my_client.get_work()
    my_client.split_pros()
    while True:
        try:
            msg = my_client.socket.get_msg(5).decode()
            if msg != b"":
                print(msg)
                if "close all" in msg:
                    for p in my_client.pros_list:
                        p.kill()
                    my_client.disconnect()
                    break
                if "range_max" and "chunk" in msg:
                    msg = json.loads(msg)
                    print("got more work")
                    my_client.set_selfs(msg)
                    print(my_client.pros_list)
                    my_client.split_pros()
        except TimeoutError:
            if any([p.is_alive() for p in my_client.pros_list]):
                continue
            else:
                my_client.socket.send_msg(f"done searching , not found ".encode())
                print("done searching , not found ")
                print("need more work")
                my_client.get_work()
                my_client.split_pros()


if __name__ == '__main__':
    main()
