import multiprocessing
import matplotlib.pyplot as plt
import numpy as np
import time

class Plotter:
    def __init__(self):
        self.data_write = np.random.random()  # Example data source
        self.queue = multiprocessing.Queue()

    def live_plot(self, queue):
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
        def update_plot():
            nonlocal x_data, y_data, x_count, x_max

            while not queue.empty():
                data_point = queue.get()
                x_data.append(x_count)
                y_data.append(data_point)

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
        update_plot()

        # Update the plot periodically with the latest data
        while True:
            update_plot()

    def generate_data(self):
        while True:
            self.data_write = np.random.random()  # Simulating data write
            self.queue.put(self.data_write)
            time.sleep(0.00001)

    def start(self):
        live_plot_process = multiprocessing.Process(target=self.live_plot, args=(self.queue,))
        live_plot_process.start()

        data_gen_process = multiprocessing.Process(target=self.generate_data)
        data_gen_process.start()


if __name__ == "__main__":
    plotter = Plotter()
    plotter.start()
