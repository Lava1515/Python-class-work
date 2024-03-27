
import tkinter as tk
import threading
import time
import serial
from PIL import Image, ImageTk

# Function to read BPM from Arduino

def get_bpm(ser):
    sum_bpm = 0
    count = 0
    ok = True
    now = time.perf_counter()
    try:
        while True:
            response = ser.readline().decode("utf-8").strip()
            if response:
                data = response.split(",")[-1]
                time.sleep(0.02)
                if ok and int(data) == 347:
                    then = now
                    now = time.perf_counter()
                    count += 1
                    bpm = 60 / (now - then)
                    if (bpm - 10) > sum_bpm > (bpm + 10):
                        if sum_bpm == 0:
                            sum_bpm = bpm
                        sum_bpm = (sum_bpm + bpm)/2
                        bpm_label.config(text=f"BPM: {bpm:.2f}")
                    ok = False
                elif not ok and int(data) < 347:
                    ok = True
    except Exception as e:
        print(e)
    finally:
        ser.close()

# Function to handle button click events

def button_click():
    option = option_var.get()
    send_option(option)

# Load background image
background_image = Image.open("webroot/images/beach_sunset.png")

# Create the GUI window
root = tk.Tk()
root.title("Client GUI")
root.geometry("800x600")  # Initial size

# Display background image
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0)

# Create and place option menu
option_var = tk.StringVar(root)
option_var.set("Option 1")
option_menu = tk.OptionMenu(root, option_var, "Option 1", "Option 2", "Option 3")
option_menu.place(relx=0.1, rely=0.1)

# Create and place submit button
submit_button = tk.Button(root, text="Submit", command=button_click)
submit_button.place(relx=0.1, rely=0.2)

# Create BPM label
bpm_label = tk.Label(root, text="BPM: ")
bpm_label.place(relx=0.1, rely=0.3)

# Serial port configuration
ser_arduino = serial.Serial("COM3", 115200, timeout=1)

# Create thread for Arduino BPM reading
t_get_bpm = threading.Thread(target=get_bpm, args=(ser_arduino,), daemon=True)
t_get_bpm.start()

# Run the GUI event loop
root.mainloop()
