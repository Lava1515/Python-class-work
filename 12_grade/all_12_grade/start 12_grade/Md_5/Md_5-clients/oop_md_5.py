import multiprocessing
from multiprocessing import Process
import hashlib
import threading
import time

Done = False


class md_5_server:

    def __init__(self, p):
        # self.target_hash = "EC9C0F7EDCC18A98B1F31853B1813301"
        # self.prosses_num = int(multiprocessing.cpu_count() * 0.70)
        # self.target_hash = "eb527dbb4435cacb2cb934dcc3c5843f" # 2272727298
        self.prosses_num = 10
        self.target_hash = "258a6572353ffd0e40a876008ef9ae3e"  # 3000100000
        self.pros = p
        self.chuncks = 10000000000 // self.prosses_num
        self.start = 0

    def md_5(self):
        global Done
        for i in range(self.chuncks):
            # print("prosses", self.pros)
            input_string = int(f"{self.pros* self.chuncks}")
            input_string += i
            # print("the num", input_string)
            hash_attempt = hashlib.md5(str(input_string).encode()).hexdigest()
            # print(hash_attempt)
            if str(hash_attempt) == self.target_hash:
                Done = True
                print(f"Original input: {input_string}")
                break


def finish(lst):
    global Done
    running = True
    while running:
        print(Done)
        if Done:
            print("finished")
            running = False
        time.sleep(3)
    for i in lst:
        i[1].kill()


if __name__ == '__main__':
    lst_t = []
    for i in range(int(multiprocessing.cpu_count() * 0.80)):
        server = md_5_server(i)
        p = Process(target=server.md_5)
        p.start()
        tup = (server, p)
        lst_t.append(tup)
    t = threading.Thread(target=finish, args=[lst_t], daemon=True)
    t.start()

