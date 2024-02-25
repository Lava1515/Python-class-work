import socket
import tkinter as tk
from protocol import Protocol
from PIL import Image, ImageTk

# Server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

# Create a Protocol instance
client_protocol = Protocol()

# Connect to the server
client_protocol.connect((SERVER_HOST, SERVER_PORT))

# Function to send selected option to the server
def send_option(option):
    client_protocol.send_msg(option.encode("utf-8"))

# Function to handle button click events
def button_click():
    option = option_var.get()
    send_option(option)

# Load background image
background_image = Image.open("../../webroot/images/beach_sunset.png")

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

# Run the GUI event loop
root.mainloop()

# Close the connection
client_protocol.close()
