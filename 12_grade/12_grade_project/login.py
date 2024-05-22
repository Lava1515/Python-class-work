import multiprocessing
import socket
import threading
import time
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring

import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
import time
import serial

from protocol import Protocol
from WebSockets import Web_Socket


class WebSocket(Web_Socket):
    def __init__(self):
        super().__init__()
        self.client_name = None
        self.ip = None
        self.random_str = None

    def handle_client(self, client_socket):
        self.accept_connection(client_socket)
        self.client_name, self.ip, self.random_str = self.receive_data(client_socket).split("//")
        print(self.client_name, self.ip, self.random_str)

    def start_websockets(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', 8080))
        server_socket.listen()

        print("WebSocket server running on port 8080")
        # accept only one client cus its only lookback
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        self.handle_client(client_socket)
        print(".client_name", self.client_name)
        return client_socket


class Client:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5555
        self.socket = Protocol()

        self.WebSocket = WebSocket()
        self.client_socket = self.WebSocket.start_websockets()
        print("WebSocket.client_name", self.WebSocket.client_name)
        if not self.connect():
            self.WebSocket.send_data(self.client_socket, "Error: Failed to connect to the server")
            messagebox.showerror("Error", "Failed to connect to the server")
            return

        DesktopApp(self.socket, self.WebSocket.client_name)

    def connect(self):
        try:
            print(self.host, self.port)
            self.socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def send_login_details(self, username, password):
        try:
            self.socket.send_msg(f"Login:{username},{password}")
            response = self.socket.get_msg().decode()
            return response
        except Exception as e:
            print(f"Error during communication: {e}")
            return "Error"


class DesktopApp:
    def __init__(self, _socket, username):
        self.username = username
        self.socket = _socket
        self.data_write = 0
        self.threads = []
        self.parent_conn, self.child_conn = multiprocessing.Pipe()

        self.root = tk.Tk()
        self.root.title("12 Grade Project")
        self.root.geometry("450x400")
        self.root.configure(bg="#6b0202")
        self.bpm_label = None
        self.run_functionality()
        self.root.mainloop()

    @staticmethod
    def get_ip():
        # :todo get the server ip
        ip = None
        # ip = askstring("IP Address", "Enter the IP address of the server:")
        return ip

    def send_bpm(self, bpm):
        try:
            self.bpm_label.config(text=bpm)
            self.socket.send_msg("bpm:" + bpm)
        except Exception as e:
            print(e)

    def mock_heartrate(self):
        heartrate = ['365']
        last_ten = []
        avg_bmps = []
        now = time.perf_counter()
        then = now
        i = 0
        count = 0
        ok = True
        while True:
            data = int(heartrate[i])
            self.parent_conn.send(data)
            if len(last_ten) >= 50:
                last_ten.pop(0)
            last_ten.append(data)
            avg = int(sum(last_ten) / len(last_ten))
            if ok and data >= avg + 3:
                then = now
                now = time.perf_counter()
                if int(60 / (now - then)) > 220:
                    continue
                count += 1
                print("heartbeat", count)
                if len(avg_bmps) >= 60:
                    avg_bmps.pop(0)
                avg_bmps.append(60 / (now - then))
                self.send_bpm(str(int(60 / (now - then))))
                print("avg", sum(avg_bmps) / len(avg_bmps))
                ok = False
            elif not ok:
                now = time.perf_counter()
                if int(60 / (now - then)) < 220 and data <= avg + 3:
                    ok = True
            i += 1
            if i == len(heartrate):
                i = 0
            time.sleep(0.02)

    def get_bpm(self):
        serW = serial.Serial("COM4", 115200, timeout=1)
        ser = serial.Serial("COM3", 115200, timeout=1)
        avg_bmps = []
        last_ten = []
        count = 0
        ok = True
        now = time.perf_counter()
        then = now
        try:
            while True:
                response = ser.readline().decode("utf-8").strip()
                if response:
                    data = int(response.split(",")[-1])
                    serW.write(response.encode() + b'\n')
                    self.data_write = data
                    self.parent_conn.send(data)
                    if len(last_ten) >= 50:
                        last_ten.pop(0)
                    last_ten.append(data)
                    avg = int(sum(last_ten) / len(last_ten))
                    if ok and data >= avg + 3:
                        then = now
                        now = time.perf_counter()
                        if int(60 / (now - then)) > 220:
                            continue
                        count += 1
                        print("heartbeat", count)
                        if len(avg_bmps) >= 60:
                            avg_bmps.pop(0)
                        avg_bmps.append(60 / (now - then))
                        bpm = 60 / (now - then)
                        print("bpm", bpm)
                        print("avg", sum(avg_bmps) / len(avg_bmps))
                        ok = False
                    elif not ok:
                        now = time.perf_counter()
                        if int(60 / (now - then)) < 220 and data <= avg + 3:
                            ok = True
        finally:
            ser.close()

    def run_functionality(self):
        self.additional_bmp_window()
        get_bpm_thread = threading.Thread(target=self.mock_heartrate)
        get_bpm_thread.start()
        self.threads.append(get_bpm_thread)

        live_plot_process = multiprocessing.Process(target=self.live_plot, args=(self.child_conn,))
        live_plot_process.start()

    @staticmethod
    def live_plot(pipe_conn):
        x_data = []
        y_data = []

        fig, ax = plt.subplots()
        line, = ax.plot([], [], lw=2)
        x_count = 0
        x_max = 60
        ax.set_xlim(x_count, x_max)

        def update_plot():
            nonlocal x_data, y_data, x_count, x_max

            while pipe_conn.poll():
                data_point = pipe_conn.recv()
                x_data.append(x_count)
                y_data.append(data_point)

                if len(x_data) > 60:
                    x_data.pop(0)
                    y_data.pop(0)

                line.set_data(x_data, y_data)
                x_count += 1
                if x_max - 10 == x_count:
                    x_max += 1
                ax.set_xlim(x_max - 60, x_max)

                avg_y = np.mean(y_data)
                ax.set_ylim(avg_y - 15, avg_y + 25)
                fig.canvas.draw()
                plt.pause(0.00001)

        update_plot()
        while True:
            update_plot()

    def additional_bmp_window(self):
        logedas = tk.Label(self.root, text="Logged as, " + self.username, font=("Arial", 14), bg="#6b0202", fg="white")
        logedas.pack(pady=5)
        bmp_label = tk.Label(self.root, text="Bpm", font=("Arial", 14), bg="#6b0202", fg="white")
        bmp_label.pack(pady=5)
        self.bpm_label = tk.Label(self.root, text="0", font=("Arial", 14), bg="#6b0202", fg="white")
        self.bpm_label.pack(pady=5)

    def on_closing(self):
        # Handle any cleanup here
        for thread in self.threads:
            if thread.is_alive():
                thread.join()  # Adjust the timeout as needed
        self.root.destroy()


if __name__ == "__main__":
    Client()
