import socket
import threading
import time
import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
import numpy as np
import serial

from WebSockets import Web_Socket  # ik know there is built in module
from protocol import Protocol


run_ = True


class Client:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 5555
        self.socket = Protocol()
        self.WebSocket = WebSocket()
        self.client_socket = self.WebSocket.start_websockets()
        if not self.connect():
            self.WebSocket.send_data(self.client_socket, "Error: Failed to connect to the server")
            messagebox.showerror("Error", "Failed to connect to the server")
            return

        ok, res = self.confirm_ip(self.WebSocket.client_name, self.WebSocket.random_str)
        if ok:
            DesktopApp(self.socket, self.WebSocket)

    def connect(self):
        try:
            print(self.host, self.port)
            self.socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def confirm_ip(self, username, random_str):
        try:
            self.socket.send_msg(f"confirm_ip:{username},{random_str}")
            response = self.socket.get_msg().decode()
            return True, response
        except Exception as e:
            print(f"Error during communication: {e}")
            return "Error", None


class WebSocket(Web_Socket):
    def __init__(self):
        super().__init__()
        self.client_name = None
        self.ip = None
        self.random_str = None
        self.client_socket = None

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
        self.client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        self.handle_client(self.client_socket)
        t = threading.Thread(target=self.queting_)
        t.start()

        return self.client_socket

    def queting_(self):
        while True:
            data = self.receive_data(self.client_socket)
            if data == "close":
                global run_
                run_ = False
                quit()


class DesktopApp:
    def __init__(self, _socket, _WebSocket):
        self._WebSocket = _WebSocket
        self.username = self._WebSocket.client_name
        self.socket = _socket
        self.data_write = 0
        self.threads = []

        t = threading.Thread(target=self.on_closing)
        t.start()
        self.threads.append(t)
        # Tk inter self's
        self.root = tk.Tk()
        self.root.title("12 Grade Project")
        self.root.geometry("450x400")
        self.root.configure(bg="#6b0202")
        self.bpm_label = None

        self.additional_bmp_window()

        # plt inter self's
        self.x_data = []
        self.y_data = []
        # Initialize figure and axis
        self.fig, self.ax = plt.subplots()
        # Initialize plot with empty data
        self.line, = self.ax.plot([], [], lw=2)
        # Set initial x-axis limits
        self.x_count = 0
        self.x_max = 60
        self.ax.set_xlim(self.x_count, self.x_max)

        self.live_plot_init()
        self.root.mainloop()

    def send_bpm(self, bpm):
        self.bpm_label.config(text=bpm)
        self.socket.send_msg(f"bpm:{self.username},{bpm}")
        self._WebSocket.send_data(self._WebSocket.client_socket, f"bpm:{self.username},{bpm}")

    def mock_heartrate(self):
        global run_
        heartrate = ['365', '369', '370', '365', '358', '351', '344', '340', '343', '345', '350', '357', '365', '369',
                     '370',
                     '365', '358', '351', '344', '340', '343', '345', '350', '357', '365', '369', '370', '365', '358',
                     '351',
                     '344', '340', '360', '352', '345', '340', '337', '336', '337', '338', '340', '342', '344', '345',
                     '346',
                     '346', '345', '344', '342', '341', '341', '341', '340', '340', '340', '340', '340', '341', '342',
                     '342',
                     '343', '342', '342', '342', '342', '342', '342', '342', '343', '343', '347', '352', '360', '367',
                     '369',
                     '366', '361', '353', '346', '341', '338', '336', '336', '338', '339', '343', '344', '346', '347',
                     '347',
                     '346', '344', '342', '341', '340', '339', '339', '339', '340', '340', '340', '342', '342', '342',
                     '343',
                     '343', '343', '343', '343', '342', '342', '342', '342', '344', '348', '354', '362', '368', '368',
                     '365',
                     '359', '351', '345', '340', '336', '335', '336', '338', '341', '343', '346', '347', '347', '347',
                     '345',
                     '344', '342', '341', '339', '339', '339', '339', '340', '340', '341', '342', '343', '343', '343',
                     '343',
                     '343', '343', '343', '343', '342', '342', '342', '345', '350', '357', '364', '368', '368', '364',
                     '357',
                     '349', '342', '338', '335', '334', '335', '338', '341', '344', '347', '349', '349', '348', '346',
                     '344',
                     '343', '341', '340', '340', '340', '339', '341', '342', '343', '343', '344', '343', '343', '343',
                     '344',
                     '344', '344', '348', '355', '362', '367', '369', '365', '360', '352', '344', '339', '335', '334',
                     '335',
                     '337', '340', '343', '346', '349', '349', '348', '346', '344', '342', '340', '339', '339', '338',
                     '340',
                     '340', '341', '342', '343', '344', '343', '344', '344', '344', '342', '344', '349', '356', '364',
                     '368',
                     '368', '364', '357', '350', '343', '338', '336', '335', '337', '338', '341', '344', '346', '347',
                     '347',
                     '347', '346', '344', '343', '341', '341', '340', '340', '340', '341', '341', '341', '343', '343',
                     '344',
                     '343', '344', '343', '343', '343', '345', '350', '357', '364', '367', '367', '362', '356', '349',
                     '342',
                     '339', '336', '336', '337', '340', '342', '344', '346', '347', '347', '346', '345', '343', '342',
                     '341',
                     '340', '339', '340', '340', '341', '341', '342', '343', '343', '344', '343', '343', '343', '343',
                     '342',
                     '342', '343', '347', '352', '359', '365', '368', '366', '361', '354', '348', '342', '338', '336',
                     '336',
                     '338', '340', '344', '346', '348', '349', '349', '347', '344', '342', '341', '340', '339', '341',
                     '341',
                     '341', '343', '344', '344', '343', '344', '343', '343', '343', '343', '342', '343', '345', '350',
                     '358',
                     '365', '368', '367', '362', '354', '347', '342', '338', '337', '337', '339', '340', '343', '345',
                     '346',
                     '347', '346', '346', '344', '342', '341', '341', '340', '340', '340', '341', '341', '342', '342',
                     '343',
                     '343', '343', '343', '343', '343', '343', '343', '342', '343', '346', '353', '360', '365', '367',
                     '366',
                     '359', '352', '344', '339', '336', '335', '336', '338', '341', '343', '345', '346', '347', '347',
                     '346',
                     '345', '342', '340', '340', '339', '340', '340', '341', '341', '342', '342', '342', '343', '344',
                     '343',
                     '343', '343', '343', '343', '343', '342', '343', '345', '351', '358', '364', '366', '364', '360',
                     '353',
                     '346', '341', '337', '335', '335', '337', '340', '343', '345', '347', '348', '348', '345', '344',
                     '342',
                     '340', '339', '339', '339', '340', '341', '341', '342', '342', '343', '343', '343', '343', '343',
                     '343',
                     '343', '343', '343', '342', '345', '350', '356', '362', '365', '364', '361', '355', '348', '341',
                     '338',
                     '335', '335', '336', '339', '342', '345', '347', '348', '347', '347', '344', '342', '341', '340',
                     '340',
                     '339', '340', '341', '341', '342', '342', '342', '343', '343', '343', '343', '343', '343', '343',
                     '344',
                     '349', '354', '360', '365', '365', '362', '357', '352', '345', '341', '339', '337', '338', '340',
                     '342',
                     '344', '345', '346', '346', '345', '344', '344', '342', '341', '340', '340', '340', '340', '341',
                     '341',
                     '341', '342', '342', '343', '343', '343', '343', '343', '343', '343', '343', '345', '348', '353',
                     '359',
                     '363', '364', '361', '356', '352', '346', '342', '340', '339', '339', '340', '342', '344', '344',
                     '345',
                     '346', '345', '344', '343', '342', '341', '341', '340', '341', '341', '341', '342', '342', '342',
                     '342',
                     '343', '343', '343', '343', '343', '342', '342', '342', '343', '345', '348', '352', '357', '358',
                     '358',
                     '356', '351', '347', '344', '341', '340', '340', '340', '341', '343', '344', '345', '346', '345',
                     '345',
                     '344', '342', '342', '341', '342', '341', '340', '341', '341', '342', '342', '342', '342', '344',
                     '343',
                     '343', '343', '342', '343', '343', '344', '347', '351', '354', '357', '357', '355', '352', '349',
                     '346',
                     '343', '342', '342', '342', '342', '343', '344', '345', '345', '345', '345', '344', '344', '343',
                     '342',
                     '342', '342', '342', '342', '342', '342', '343', '343', '343', '343', '344', '344', '344', '344',
                     '344',
                     '343', '343', '343', '343', '344', '347', '351', '354', '358', '359', '358', '356', '352', '349',
                     '346',
                     '344', '344', '344', '344', '345', '346', '346', '346', '346', '346', '344', '344', '343', '342',
                     '342',
                     '343', '342', '342', '343', '343', '343', '343', '344', '344', '344', '344', '343', '343', '343',
                     '343',
                     '343', '344', '343', '343', '343', '344', '346', '351', '357', '364', '367', '367', '364', '358',
                     '352',
                     '347', '342', '340', '339', '340', '341', '342', '344', '346', '346', '346', '346', '345', '343',
                     '341',
                     '341', '341', '340', '341', '341', '341', '342', '342', '343', '343', '343', '343', '344', '343',
                     '343',
                     '342', '342', '343', '342', '342', '342', '343', '345', '350', '356', '363', '369', '370', '366',
                     '360',
                     '351', '346', '342', '338', '337', '338', '339', '342', '344', '346', '348', '348', '347', '346',
                     '344',
                     '342', '341', '340', '340', '341', '341', '342', '342', '342', '343', '342', '343', '343', '343',
                     '342',
                     '343', '343', '342', '342', '344', '348', '355', '363', '367', '369', '366', '359', '352', '345',
                     '340',
                     '338', '337', '338', '339', '342', '345', '346', '347', '348', '346', '346', '344', '342', '341',
                     '340',
                     '340', '340', '341', '341', '341', '342', '342', '343', '343', '343', '343', '343', '343', '343',
                     '343',
                     '342', '342', '343', '345', '350', '358', '364', '368', '367', '362', '355', '347', '342', '338',
                     '336',
                     '336', '338', '340', '343', '345', '346', '348', '348', '347', '345', '343', '341', '340', '340',
                     '340',
                     '340', '340', '341', '341', '342', '343', '343', '344', '344', '343', '344', '344', '343', '342',
                     '343',
                     '342', '344', '347', '352', '361', '365', '368', '365', '359', '351', '345', '339', '336', '335',
                     '336',
                     '337', '340', '343', '346', '348', '348', '348', '347', '344', '343', '341', '340', '340', '340',
                     '339',
                     '340', '340', '341', '342', '343', '343', '343', '343', '343', '343', '343', '343', '343', '342',
                     '342',
                     '346', '350', '357', '363', '366', '366', '361', '355', '347', '342', '338', '336', '335', '337',
                     '339',
                     '342', '345', '348', '349', '349', '348', '346', '343', '342', '340', '339', '340', '339', '340',
                     '341',
                     '341', '342', '342', '343', '343', '344', '344', '344', '344', '344', '343', '344', '347', '353',
                     '360',
                     '365', '366', '364', '359', '352', '346', '340', '337', '334', '335', '337', '340', '345', '347',
                     '349',
                     '350', '349', '347', '345', '343', '341', '340', '340', '339', '340', '341', '341', '342', '343',
                     '343',
                     '344', '344', '344', '343', '344', '346', '351', '357', '363', '367', '366', '361', '355', '348',
                     '342',
                     '338', '336', '336', '338', '340', '343', '346', '348', '349', '348', '347', '345', '343', '341',
                     '341',
                     '340', '339', '340', '340', '341', '342', '343', '343', '344', '344', '344', '343', '343', '342',
                     '343',
                     '344', '348', '354', '361', '367', '367', '363', '358', '351', '345', '339', '337', '336', '337',
                     '340',
                     '341', '344', '346', '347', '348', '347', '345', '344', '343', '340', '340', '340', '340', '340',
                     '340',
                     '342', '341', '343', '344', '344', '343', '344', '343', '343', '343', '342', '342', '343', '345',
                     '351',
                     '358', '364', '366', '364', '360', '353', '347', '341', '338', '336', '337', '338', '340', '343',
                     '345',
                     '347', '348', '347', '346', '345', '342', '341', '340', '340', '340', '340', '342', '342', '342',
                     '343',
                     '344', '344', '344', '344', '344', '345', '344', '343', '343', '346', '349', '355', '360', '364',
                     '363',
                     '360', '354', '347', '342', '339', '337', '336', '338', '341', '343', '345', '346', '348', '346',
                     '346',
                     '344', '343', '341', '340', '341', '340', '340', '341', '341', '341', '342', '343', '343', '344',
                     '344',
                     '344', '343', '344', '343', '342', '343', '343', '346', '352', '359', '365', '367', '365', '361',
                     '355',
                     '349', '343', '340', '339', '338', '339', '341', '343', '344', '345', '346', '346', '345', '344',
                     '343',
                     '342', '340', '341', '340', '341', '341', '341', '342', '343', '343', '344', '343', '343', '343',
                     '343',
                     '343', '343', '343', '342', '342', '342', '342', '343', '346', '352', '359', '366', '370', '368',
                     '363',
                     '356', '349', '343', '339', '337', '337', '338', '340', '343', '346', '347', '348', '348', '347',
                     '346',
                     '345', '343', '342', '341', '342', '342', '341', '341', '342', '342', '343', '342', '343', '342',
                     '342',
                     '341', '342', '341', '342', '342', '343', '342', '342', '343', '347', '352', '361', '366', '369',
                     '367',
                     '361', '352', '346', '340', '337', '335', '336', '338', '341', '343', '346', '347', '348', '348',
                     '346',
                     '344', '342', '341', '340', '339', '339', '339', '340', '341', '342', '342', '343', '343', '344',
                     '344',
                     '343', '343', '342', '343', '342', '342', '342', '342', '342', '343', '346', '353', '360', '366',
                     '368',
                     '366', '361', '354', '347', '341', '338', '336', '336', '337', '340', '344', '347', '349', '348',
                     '348',
                     '347', '345', '343', '341', '339', '339', '340', '339', '340', '341', '342', '343', '343', '343',
                     '344',
                     '344', '344', '344', '343', '343', '343', '343', '346', '351', '359', '365', '366', '364', '360',
                     '352',
                     '346', '341', '338', '336', '336', '338', '340', '342', '345', '347', '348', '348', '347', '344',
                     '344',
                     '343', '341', '341', '340', '340', '341', '341', '341', '343', '344', '343']
        last_ten = []
        avg_bmps = []
        now = time.perf_counter()
        then = now
        i = 0
        count = 0
        ok = True
        while run_:
            data = int(heartrate[i])
            self.data_write = data
            # self.parent_conn.send(data)
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
        global run_
        # serW = serial.Serial("COM4", 115200, timeout=1)
        ser = serial.Serial("COM5", 115200, timeout=1)
        avg_bmps = []
        last_ten = []
        count = 0
        ok = True
        now = time.perf_counter()
        then = now
        try:
            while run_:
                response = ser.readline().decode("utf-8").strip()
                if response:
                    data = int(response.split(",")[-1])
                    # serW.write(response.encode() + b'\n')
                    self.data_write = data
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
        finally:
            ser.close()

    def live_plot_init(self):
        # Initialize empty lists to store x and y data
        get_bpm_thread = threading.Thread(target=self.mock_heartrate)
        get_bpm_thread.start()
        self.threads.append(get_bpm_thread)

        self.live_plot_iter()
        # Function to update the plot

    def update_plot(self):

        # Append new data points
        self.x_data.append(self.x_count)
        self.y_data.append(self.data_write)

        # If more than 60 data points, remove the oldest ones
        if len(self.x_data) > 60:
            self.x_data.pop(0)
            self.y_data.pop(0)

        # Update x and y data of the plot
        self.line.set_data(self.x_data, self.y_data)

        # Update x-axis limits
        self.x_count += 2
        if self.x_max - 10 == self.x_count:
            self.x_max += 2
        self.ax.set_xlim(self.x_max - 60, self.x_max)

        # Calculate the average of the last 60 data points
        avg_y = np.mean(self.y_data)

        # Set y-axis limit dynamically based on the average
        self.ax.set_ylim(avg_y - 15, avg_y + 25)

        # Redraw the plot
        self.fig.canvas.draw()
        plt.pause(0.00001)

    def live_plot_iter(self):
        global run_
        if run_:
            self.update_plot()
            self.root.after(10, self.live_plot_iter)
        else:
            quit()

    def additional_bmp_window(self):
        logedas = tk.Label(self.root, text="Logged as, " + self.username, font=("Arial", 14), bg="#6b0202", fg="white")
        logedas.pack(pady=5)
        bmp_label = tk.Label(self.root, text="Bpm", font=("Arial", 14), bg="#6b0202", fg="white")
        bmp_label.pack(pady=5)
        self.bpm_label = tk.Label(self.root, text="0", font=("Arial", 14), bg="#6b0202", fg="white")
        self.bpm_label.pack(pady=5)

    def on_closing(self):
        global run_
        while True:
            print(run_)
            if not run_:
                # Handle any cleanup here
                print("closeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                self.close_()
            time.sleep(0.5)

    def close_(self):
        for thread in self.threads:
            if thread.is_alive():
                thread.join()  # Adjust the timeout as needed
        self.root.destroy()


if __name__ == "__main__":
    Client()
