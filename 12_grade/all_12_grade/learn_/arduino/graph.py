import threading
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

# Define the live_plot function
data_write = 0
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

# Function to create and run the Tkinter window
def run_tkinter():
    # Create Tkinter window
    root = tk.Tk()
    root.title("Tkinter Window")

    # Add widgets, etc. to the Tkinter window as needed

    # Run the Tkinter main loop
    root.mainloop()

# Create and start a thread for each function
threading.Thread(target=live_plot).start()
threading.Thread(target=run_tkinter).start()
