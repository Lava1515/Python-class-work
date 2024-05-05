import threading
import time

import matplotlib.pyplot as plt
import numpy as np
import serial

data_write = 100


def get_bpm(serW):
    global data_write
    ser = serial.Serial("COM3", 115200, timeout=1)
    avg_bmps = []
    last_ten = []
    count = 0
    avg = 0
    ok = True
    now = time.perf_counter()
    then = now
    try:
        while True:
            response = ser.readline().decode("utf-8").strip()
            if response:
                data = int(response.split(",")[-1])
                serW.write(response.encode() + b'\n')
                data_write = data  # Update global variable with the latest data
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
                    print("avg", sum(avg_bmps) / len(avg_bmps))
                    ok = False
                elif not ok:
                    now = time.perf_counter()
                    if int(60 / (now - then)) < 220 and data <= avg + 3:
                        ok = True
    finally:
        ser.close()


def live_plot():
    global data_write
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
    update_plot(data_write)

    # Update the plot periodically with the latest data
    while True:
        update_plot(data_write)


def main():
    serW = serial.Serial("COM4", 115200, timeout=1)

    # Start get_bpm function in a thread
    get_bpm_thread = threading.Thread(target=get_bpm, args=(serW,))
    get_bpm_thread.start()

    # Call live_plot function in the main thread
    live_plot()


if __name__ == "__main__":
    main()
