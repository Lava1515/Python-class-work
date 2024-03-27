import time
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
from collections import deque


def animate(i, dataList):
    arduinoData_string = ser.readline().decode('ascii')  # Decode received Arduino data as a formatted string
    print(arduinoData_string)  # 'i' is an incrementing variable based upon frames = x argument
    arduinoData_string = arduinoData_string.split(",")[-1]
    try:
        arduinoData_float = float(arduinoData_string)  # Convert to float
        dataList.append(arduinoData_float)  # Add to the list holding the fixed number of points to animate
    except ValueError:  # Pass if data point is bad
        pass

    dataList = deque(
        list(dataList)[-40:])  # Fix the list size so that the animation plot 'window' is x number of points

    ax.clear()  # Clear last data frame
    ax.plot(dataList)  # Plot new data frame

    ax.set_ylim([340, 355])  # Set Y axis limit of plot
    ax.set_title("Arduino Data")  # Set title of figure
    ax.set_ylabel("Value")  # Set title of y axis


def data_read_thread(ser, dataList):
    while True:
        arduinoData_string = ser.readline().decode('ascii')  # Decode received Arduino data as a formatted string
        print(arduinoData_string)  # 'i' is an incrementing variable based upon frames = x argument
        arduinoData_string = arduinoData_string.split(",")[-1]
        try:
            arduinoData_float = float(arduinoData_string)  # Convert to float
            dataList.append(arduinoData_float)  # Add to the list holding the fixed number of points to animate
        except ValueError:  # Pass if data point is bad
            pass

        dataList = deque(
            list(dataList)[-40:])  # Fix the list size so that the animation plot 'window' is x number of points
        time.sleep(0.1)


def main():
    # Create empty list variable for later use
    dataList = deque(maxlen=40)

    fig = plt.figure()  # Create Matplotlib plots fig is the 'higher level' plot window
    ax = fig.add_subplot(111)  # Add subplot to main fig window

    ser = serial.Serial("COM3",
                        115200)  # Establish Serial object with COM port and BAUD rate to match Arduino Port/rate
    time.sleep(2)  # Time delay for Arduino Serial initialization

    # Matplotlib Animation Function that takes care of real-time plot.
    # Note that 'fargs' parameter is where we pass in our dataList.
    ani = animation.FuncAnimation(fig, animate, fargs=(dataList,), interval=100)

    # Create a separate thread for reading data from the serial port
    thread = threading.Thread(target=data_read_thread, args=(dataList,))
    thread.daemon = True
    thread.start()

    plt.show()  # Keep Matplotlib plot persistent on screen until it is closed
    ser.close()  # Close Serial connection when plot is closed
