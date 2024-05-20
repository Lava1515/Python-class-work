import queue
import threading
import time
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring

import matplotlib.pyplot as plt
import numpy as np
import serial

from protocol import Protocol


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.protocol = Protocol()

    def connect(self):
        try:
            self.protocol.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def send_login_details(self, username, password):
        try:
            self.protocol.send_msg(f"Login:{username},{password}")
            response = self.protocol.get_msg().decode()
            return response
        except Exception as e:
            print(f"Error during communication: {e}")
            return "Error"


class DesktopApp:
    def __init__(self):
        self.username = None
        self.data_write = 0
        self.host = self.get_ip()
        if not self.host:
            self.host = 'localhost'  # Default to localhost if no IP provided

        self.client = Client(self.host, 5555)
        if not self.client.connect():
            messagebox.showerror("Error", "Failed to connect to the server")
            return

        self.root = tk.Tk()
        self.root.title("12 Grade Project")
        self.root.geometry("450x400")
        self.root.configure(bg="#6b0202")

        # Bind the close event to the custom exit function
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.title_label = tk.Label(self.root, text="Login", font=("Arial", 24), bg="#6b0202", fg="white")
        self.title_label.pack(pady=20)

        self.username_label = tk.Label(self.root, text="Username", font=("Arial", 14), bg="#6b0202", fg="white")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 14))
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password", font=("Arial", 14), bg="#6b0202", fg="white")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=5)

        self.eye_button = tk.Button(self.root, text="Show", command=self.toggle_password, bg="#6b0202", fg="white")
        self.eye_button.pack(pady=5)

        self.submit_button = tk.Button(self.root, text="Submit", command=self.submit, bg="#f48403", fg="white")
        self.submit_button.pack(pady=20)

        self.message_label = tk.Label(self.root, font=("Arial", 12), bg="#6b0202", fg="yellow")
        self.message_label.pack(pady=5)

        self.bpm_label = None

        self.threads = []

        self.root.mainloop()

    @staticmethod
    def get_ip():
        ip = askstring("IP Address", "Enter the IP address of the server:")
        return ip

    def toggle_password(self):
        if self.password_entry.cget('show') == '*':
            self.password_entry.config(show='')
            self.eye_button.config(text="Hide")
        else:
            self.password_entry.config(show='*')
            self.eye_button.config(text="Show")

    def submit(self):
        # Clear previous message
        self.message_label.config(text="")

        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username:
            self.message_label.config(text="No username provided")
            return
        elif not password:
            self.message_label.config(text="Password is needed")
            return

        response = self.client.send_login_details(username, password)
        if response == "Success":
            self.message_label.config(text="Logged in successfully!")
            # Destroy the login window
            widgets = [self.title_label, self.username_label, self.username_entry,
                       self.password_label, self.password_entry, self.eye_button,
                       self.submit_button, self.message_label]
            for widget in widgets:
                widget.destroy()
                print("destroyed")
            # Run the desired functionality after successful login
            self.username = username
            self.run_functionality()
        elif response == "Failure":
            self.message_label.config(text="Invalid username or password")
        else:
            self.message_label.config(text="Error during login")

    def mock_heartrate(self):
        heartrate = ['365', '369', '370', '365', '358', '351', '344', '340', '343', '345', '350', '357', '365', '369',
                     '370', '365', '358', '351', '344', '340', '343', '345', '350', '357', '365', '369', '370', '365',
                     '358', '351', '344', '340', '360', '352', '345', '340', '337', '336', '337', '338', '340', '342',
                     '344', '345', '346', '346', '345', '344', '342', '341', '341', '341', '340', '340', '340', '340',
                     '340', '341', '342', '342', '343', '342', '342', '342', '342', '342', '342', '342', '343', '343',
                     '347', '352', '360', '367', '369', '366', '361', '353', '346', '341', '338', '336', '336', '338',
                     '339', '343', '344', '346', '347', '347', '346', '344', '342', '341', '340', '339', '339', '339',
                     '340', '340', '340', '342', '342', '342', '343', '343', '343', '343', '343', '342', '342', '342',
                     '342', '344', '348', '354', '362', '368', '368', '365', '359', '351', '345', '340', '336', '335',
                     '336', '338', '341', '343', '346', '347', '347', '347', '345', '344', '342', '341', '339', '339',
                     '339', '339', '340', '340', '341', '342', '343', '343', '343', '343', '343', '343', '343', '343',
                     '342', '342', '342', '345', '350', '357', '364', '368', '368', '364', '357', '349', '342', '338',
                     '335', '334', '335', '338', '341', '344', '347', '349', '349', '348', '346', '344', '343', '341',
                     '340', '340', '340', '339', '341', '342', '343', '343', '344', '343', '343', '343', '344', '344',
                     '344', '348', '355', '362', '367', '369', '365', '360', '352', '344', '339', '335', '334', '335',
                     '337', '340', '343', '346', '349', '349', '348', '346', '344', '342', '340', '339', '339', '338',
                     '340', '340', '341', '342', '343', '344', '343', '344', '344', '344', '342', '344', '349', '356',
                     '364', '368', '368', '364', '357', '350', '343', '338', '336', '335', '337', '338', '341', '344',
                     '346', '347', '347', '347', '346', '344', '343', '341', '341', '340', '340', '340', '341', '341',
                     '341', '343', '343', '344', '343', '344', '343', '343', '343', '345', '350', '357', '364', '367',
                     '367', '362', '356', '349', '342', '339', '336', '336', '337', '340', '342', '344', '346', '347',
                     '347', '346', '345', '343', '342', '341', '340', '339', '340', '340', '341', '341', '342', '343',
                     '343', '344', '343', '343', '343', '343', '342', '342', '343', '347', '352', '359', '365', '368',
                     '366', '361', '354', '348', '342', '338', '336', '336', '338', '340', '344', '346', '348', '349',
                     '349', '347', '344', '342', '341', '340', '339', '341', '341', '341', '343', '344', '344', '343',
                     '344', '343', '343', '343', '343', '342', '343', '345', '350', '358', '365', '368', '367', '362',
                     '354', '347', '342', '338', '337', '337', '339', '340', '343', '345', '346', '347', '346', '346',
                     '344', '342', '341', '341', '340', '340', '340', '341', '341', '342', '342', '343', '343', '343',
                     '343', '343', '343', '343', '343', '342', '343', '346', '353', '360', '365', '367', '366', '359',
                     '352', '344', '339', '336', '335', '336', '338', '341', '343', '345', '346', '347', '347', '346',
                     '345', '342', '340', '340', '339', '340', '340', '341', '341', '342', '342', '342', '343', '344',
                     '343', '343', '343', '343', '343', '343', '342', '343', '345', '351', '358', '364', '366', '364',
                     '360', '353', '346', '341', '337', '335', '335', '337', '340', '343', '345', '347', '348', '348',
                     '345', '344', '342', '340', '339', '339', '339', '340', '341', '341', '342', '342', '343', '343',
                     '343', '343', '343', '343', '343', '343', '343', '342', '345', '350', '356', '362', '365', '364',
                     '361', '355', '348', '341', '338', '335', '335', '336', '339', '342', '345', '347', '348', '347',
                     '347', '344', '342', '341', '340', '340', '339', '340', '341', '341', '342', '342', '342', '343',
                     '343', '343', '343', '343', '343', '343', '344', '349', '354', '360', '365', '365', '362', '357',
                     '352', '345', '341', '339', '337', '338', '340', '342', '344', '345', '346', '346', '345', '344',
                     '344', '342', '341', '340', '340', '340', '340', '341', '341', '341', '342', '342', '343', '343',
                     '343', '343', '343', '343', '343', '343', '345', '348', '353', '359', '363', '364', '361', '356',
                     '352', '346', '342', '340', '339', '339', '340', '342', '344', '344', '345', '346', '345', '344',
                     '343', '342', '341', '341', '340', '341', '341', '341', '342', '342', '342', '342', '343', '343',
                     '343', '343', '343', '342', '342', '342', '343', '345', '348', '352', '357', '358', '358', '356',
                     '351', '347', '344', '341', '340', '340', '340', '341', '343', '344', '345', '346', '345', '345',
                     '344', '342', '342', '341', '342', '341', '340', '341', '341', '342', '342', '342', '342', '344',
                     '343', '343', '343', '342', '343', '343', '344', '347', '351', '354', '357', '357', '355', '352',
                     '349', '346', '343', '342', '342', '342', '342', '343', '344', '345', '345', '345', '345', '344',
                     '344', '343', '342', '342', '342', '342', '342', '342', '342', '343', '343', '343', '343', '344',
                     '344', '344', '344', '344', '343', '343', '343', '343', '344', '347', '351', '354', '358', '359',
                     '358', '356', '352', '349', '346', '344', '344', '344', '344', '345', '346', '346', '346', '346',
                     '346', '344', '344', '343', '342', '342', '343', '342', '342', '343', '343', '343', '343', '344',
                     '344', '344', '344', '343', '343', '343', '343', '343', '344', '343', '343', '343', '344', '346',
                     '351', '357', '364', '367', '367', '364', '358', '352', '347', '342', '340', '339', '340', '341',
                     '342', '344', '346', '346', '346', '346', '345', '343', '341', '341', '341', '340', '341', '341',
                     '341', '342', '342', '343', '343', '343', '343', '344', '343', '343', '342', '342', '343', '342',
                     '342', '342', '343', '345', '350', '356', '363', '369', '370', '366', '360', '351', '346', '342',
                     '338', '337', '338', '339', '342', '344', '346', '348', '348', '347', '346', '344', '342', '341',
                     '340', '340', '341', '341', '342', '342', '342', '343', '342', '343', '343', '343', '342', '343',
                     '343', '342', '342', '344', '348', '355', '363', '367', '369', '366', '359', '352', '345', '340',
                     '338', '337', '338', '339', '342', '345', '346', '347', '348', '346', '346', '344', '342', '341',
                     '340', '340', '340', '341', '341', '341', '342', '342', '343', '343', '343', '343', '343', '343',
                     '343', '343', '342', '342', '343', '345', '350', '358', '364', '368', '367', '362', '355', '347',
                     '342', '338', '336', '336', '338', '340', '343', '345', '346', '348', '348', '347', '345', '343',
                     '341', '340', '340', '340', '340', '340', '341', '341', '342', '343', '343', '344', '344', '343',
                     '344', '344', '343', '342', '343', '342', '344', '347', '352', '361', '365', '368', '365', '359',
                     '351', '345', '339', '336', '335', '336', '337', '340', '343', '346', '348', '348', '348', '347',
                     '344', '343', '341', '340', '340', '340', '339', '340', '340', '341', '342', '343', '343', '343',
                     '343', '343', '343', '343', '343', '343', '342', '342', '346', '350', '357', '363', '366', '366',
                     '361', '355', '347', '342', '338', '336', '335', '337', '339', '342', '345', '348', '349', '349',
                     '348', '346', '343', '342', '340', '339', '340', '339', '340', '341', '341', '342', '342', '343',
                     '343', '344', '344', '344', '344', '344', '343', '344', '347', '353', '360', '365', '366', '364',
                     '359', '352', '346', '340', '337', '334', '335', '337', '340', '345', '347', '349', '350', '349',
                     '347', '345', '343', '341', '340', '340', '339', '340', '341', '341', '342', '343', '343', '344',
                     '344', '344', '343', '344', '346', '351', '357', '363', '367', '366', '361', '355', '348', '342',
                     '338', '336', '336', '338', '340', '343', '346', '348', '349', '348', '347', '345', '343', '341',
                     '341', '340', '339', '340', '340', '341', '342', '343', '343', '344', '344', '344', '343', '343',
                     '342', '343', '344', '348', '354', '361', '367', '367', '363', '358', '351', '345', '339', '337',
                     '336', '337', '340', '341', '344', '346', '347', '348', '347', '345', '344', '343', '340', '340',
                     '340', '340', '340', '340', '342', '341', '343', '344', '344', '343', '344', '343', '343', '343',
                     '342', '342', '343', '345', '351', '358', '364', '366', '364', '360', '353', '347', '341', '338',
                     '336', '337', '338', '340', '343', '345', '347', '348', '347', '346', '345', '342', '341', '340',
                     '340', '340', '340', '342', '342', '342', '343', '344', '344', '344', '344', '344', '345', '344',
                     '343', '343', '346', '349', '355', '360', '364', '363', '360', '354', '347', '342', '339', '337',
                     '336', '338', '341', '343', '345', '346', '348', '346', '346', '344', '343', '341', '340', '341',
                     '340', '340', '341', '341', '341', '342', '343', '343', '344', '344', '344', '343', '344', '343',
                     '342', '343', '343', '346', '352', '359', '365', '367', '365', '361', '355', '349', '343', '340',
                     '339', '338', '339', '341', '343', '344', '345', '346', '346', '345', '344', '343', '342', '340',
                     '341', '340', '341', '341', '341', '342', '343', '343', '344', '343', '343', '343', '343', '343',
                     '343', '343', '342', '342', '342', '342', '343', '346', '352', '359', '366', '370', '368', '363',
                     '356', '349', '343', '339', '337', '337', '338', '340', '343', '346', '347', '348', '348', '347',
                     '346', '345', '343', '342', '341', '342', '342', '341', '341', '342', '342', '343', '342', '343',
                     '342', '342', '341', '342', '341', '342', '342', '343', '342', '342', '343', '347', '352', '361',
                     '366', '369', '367', '361', '352', '346', '340', '337', '335', '336', '338', '341', '343', '346',
                     '347', '348', '348', '346', '344', '342', '341', '340', '339', '339', '339', '340', '341', '342',
                     '342', '343', '343', '344', '344', '343', '343', '342', '343', '342', '342', '342', '342', '342',
                     '343', '346', '353', '360', '366', '368', '366', '361', '354', '347', '341', '338', '336', '336',
                     '337', '340', '344', '347', '349', '348', '348', '347', '345', '343', '341', '339', '339', '340',
                     '339', '340', '341', '342', '343', '343', '343', '344', '344', '344', '344', '343', '343', '343',
                     '343', '346', '351', '359', '365', '366', '364', '360', '352', '346', '341', '338', '336', '336',
                     '338', '340', '342', '345', '347', '348', '348', '347', '344', '344', '343', '341', '341', '340',
                     '340', '341', '341', '341', '343', '344', '343']

        last_ten = []
        avg_bmps = []
        now = time.perf_counter()
        then = now
        i = 0
        count = 0
        ok = True
        while True:
            data = int(heartrate[i])
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
                print(60 / (now - then))
                self.bpm_label.config(text=str(int(60 / (now - then))))
                print("a")
                self.client.protocol.send_msg("bpm:" + str((int(60 / (now - then)))))
                print("b")
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
                    self.data_write = data  # Update global variable with the latest data
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
        # Start get_bpm function in a thread
        get_bpm_thread = threading.Thread(target=self.mock_heartrate)
        get_bpm_thread.start()
        self.threads.append(get_bpm_thread)

        # Call live_plot function in the main thread
        live_plot_thread = threading.Thread(target=self.add_bmp_window, args=(self.username,))
        live_plot_thread.start()
        self.threads.append(live_plot_thread)

        self.live_plot()

    def live_plot(self):
        # Initialize empty lists to store x and y data
        x_data = []
        y_data = []

        # Initialize figure and axis
        fig, ax = plt.subplots()

        # Initialize plot with empty data
        line, = ax.plot([], [], lw=2)

        # Set initial x-axis limits
        x_count = 0
        x_max = 60
        ax.set_xlim(x_count, x_max)

        # Function to update the plot
        def update_plot(new_y):
            nonlocal x_data, y_data, x_count, x_max

            # Append new data points
            x_data.append(x_count)
            y_data.append(new_y)

            # If more than 60 data points, remove the oldest ones
            if len(x_data) > 60:
                x_data.pop(0)
                y_data.pop(0)

            # Update x and y data of the plot
            line.set_data(x_data, y_data)

            # Update x-axis limits
            x_count += 1
            if x_max - 10 == x_count:
                x_max += 1
            ax.set_xlim(x_max - 60, x_max)

            # Calculate the average of the last 60 data points
            avg_y = np.mean(y_data)

            # Set y-axis limit dynamically based on the average
            ax.set_ylim(avg_y - 15, avg_y + 25)

            # Redraw the plot
            fig.canvas.draw()
            plt.pause(0.00001)

        # Generate initial data for the plot
        update_plot(self.data_write)

        # Update the plot periodically with the latest data
        while True:
            update_plot(self.data_write)

    def add_bmp_window(self, username):
        logedas = tk.Label(self.root, text="Loged as, " + username, font=("Arial", 14), bg="#6b0202", fg="white")
        logedas.pack(pady=5)
        bmp_label = tk.Label(self.root, text="Bpm", font=("Arial", 14), bg="#6b0202", fg="white")
        bmp_label.pack(pady=5)
        self.bpm_label = tk.Label(self.root, text="0", font=("Arial", 14), bg="#6b0202", fg="white")
        self.bpm_label.pack(pady=5)

    def on_closing(self):
        # Handle any cleanup here
        for thread in self.threads:
            if thread.is_alive():
                thread.join(1)  # Adjust the timeout as needed
        self.root.destroy()


if __name__ == "__main__":
    DesktopApp()
