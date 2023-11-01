import threading
import time
import traceback

from protocol import Protocol
import json
import tkinter as tk
from tkinter import ttk


class md_5_server:
    def __init__(self):
        self.max_clients = 25
        self.client_cycle = 1
        self.counter = 0
        self.clients_sock = {}
        self.server_socket = Protocol()
        self.num_to_check = 10000000000
        self.chunk = self.num_to_check // self.max_clients
        self.ranges = {}
        self.who_got_range = {}
        self.lock_clients_sock = threading.Lock()
        for num in range(self.max_clients):
            self.ranges[self.chunk * num] = False
        self._label = ""

    def bind(self, ip, port):
        self.server_socket.bind((ip, port))

    def update_tk_label(self, label, progress_var):
        while True:
            label.config(text=self._label)
            if "%" in self._label:
                try:
                    progress_var.set(float(self._label.split(":")[-1][:-1]))
                except ValueError:
                    traceback.print_exc()
            time.sleep(1)

    def open_tkinter_window(self):
        root = tk.Tk()
        root.title("Current percentage")
        label = tk.Label(root, font=('Helvetica', 48))
        label.pack(pady=20)
        progress_var = tk.IntVar()
        progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
        progress_bar.pack(padx=20, pady=20, fill=tk.X)

        threading.Thread(target=self.update_tk_label, daemon=True, args=(label, progress_var)).start()
        root.mainloop()

    def listen(self):
        self.server_socket.listen()
        print("Server is up and running")
        threading.Thread(target=self.open_tkinter_window).start()

    def accept(self):
        try:
            client_sock, client_address = self.server_socket.accept()
        except TimeoutError:
            return
        self.lock_clients_sock.acquire()
        self.clients_sock[client_sock] = client_address
        self.lock_clients_sock.release()
        print('\r' + "[Server]: New Connection From: '%s:%s'" % client_address)

    def handle_client(self):
        server.server_socket.settimeout(0.005)
        found = False
        res = ""
        while not found:
            server.accept()
            self.lock_clients_sock.acquire()
            tmp_ = list(self.clients_sock.items())
            self.lock_clients_sock.release()
            for sock, addr in tmp_:
                try:
                    res = sock.get_msg().decode()
                    # print(res, "the response from ")
                    if res == "":
                        # print("none")
                        continue

                    elif "count" in res:
                        # print("count")
                        res = json.loads(res)
                        self.counter += res["count"]
                        self._label = f"current percentage :{str(self.counter * 100 / self.num_to_check)}%"
                        # print('\r' + str(self.counter) + " " + str(self.counter * 100 / self.num_to_check) + "%",
                        #       end="")

                    elif "done searching" in res:
                        # print("done searching, not found")
                        self.client_cycle += 1
                        print('\r' + "done search and need more num ", self.client_cycle)

                    elif "get work man" in res:
                        self.client_cycle = 1
                        # print(self.chunk * self.client_cycle)
                        while self.ranges[self.chunk * self.client_cycle] and self.client_cycle != self.max_clients:
                            self.client_cycle += 1
                            # print(self.client_cycle)
                        # print("normal num", self.client_cycle)
                        sock.send_msg(
                            (json.dumps({"range_max": self.chunk * self.client_cycle, "chunk": self.chunk}).encode()))
                        self.who_got_range[sock] = self.chunk * self.client_cycle
                        self.ranges[self.chunk * self.client_cycle] = True

                    elif "WE FOUND THE NUMER ITS " in res:
                        self._label = f"the number is {res.split()[5]}"
                        print('\r' + "found", addr)
                        for s in self.clients_sock:
                            s.send_msg("close all".encode())
                        found = True
                        break

                except ConnectionError:
                    # print("exeption ", res)
                    # print("cleint left ", addr)
                    if sock in self.who_got_range:
                        # print("restart range list ")
                        self.ranges[self.who_got_range[sock]] = False
                        self.who_got_range.pop(sock)
                    self.lock_clients_sock.acquire()
                    self.clients_sock.pop(sock)
                    self.lock_clients_sock.release()
                    break
            time.sleep(0.005)


if __name__ == '__main__':
    server = md_5_server()
    server.bind("0.0.0.0", 8820)
    server.listen()
    server.handle_client()
