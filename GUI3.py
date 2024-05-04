import tkinter as tk
import tkinter.font as tkFont
from Functions import *
from tkinter import messagebox
from datetime import datetime
from Communication import *
from CollectData import collect_dataset, fill_buffer
from multiprocessing import Pool
from ML import model
from Graphs import *

def show_frame(page_name):
    frame = frames[page_name]
    frame.tkraise()

def show_message(Mtype, message):
    if Mtype == "Information":
        messagebox.showinfo(Mtype, message)
    elif Mtype == "Warning":
        messagebox.showwarning(Mtype, message)
    elif Mtype == "Error":
        messagebox.showerror(Mtype, message)
    else:
        print("Invalid message type")


def GButton_295_command():
    global ser_
    global port_

    ok, ser_, port_, baudRate = [ComOK()[0], ComOK()[1], ComOK()[2], ComOK()[3]]
    if ok:
        show_message("Information", f"Port - {port_} with baud rate - {baudRate} is ready")
        GLabel_485.config(text=port_)
        GLabel_486.config(text=baudRate)
    else:
        show_message("Error", "No port found")
        GLabel_485.config(text=port_)
        GLabel_486.config(text=baudRate)

root = tk.Tk()
root.geometry("800x600")
root.title("Page Navigation")

# Container to hold all pages
container = tk.Frame(root)
container.pack(side="top", fill="both", expand=True)

# Dictionary to hold frames of all pages
frames = {}

# Define all pages
def create_page1():
    frame = tk.Frame(container)
    frame.grid(row=0, column=0, sticky="nsew")
    label = tk.Label(frame, text="Select COM Port:")
    label.pack(side="top", fill="x", pady=10)

    GButton_295 = tk.Button(root)
    GButton_295["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    GButton_295["font"] = ft
    GButton_295["fg"] = "#000000"
    GButton_295["justify"] = "center"
    GButton_295["text"] = "Start Communication"
    GButton_295.place(x=40, y=40, width=120, height=40)
    GButton_295["command"] = GButton_295_command

    # port label
    GLabel_485 = tk.Label(root)
    GLabel_485["bg"] = "#ffffff"
    ft = tkFont.Font(family='Times', size=10)
    GLabel_485["font"] = ft
    GLabel_485["fg"] = "#333333"
    GLabel_485["justify"] = "left"
    GLabel_485["text"] = ""
    GLabel_485.place(x=200, y=40, width=120, height=40)

    # baud rate label
    GLabel_486 = tk.Label(root)
    GLabel_486["bg"] = "#ffffff"
    ft = tkFont.Font(family='Times', size=10)
    GLabel_486["font"] = ft
    GLabel_486["fg"] = "#333333"
    GLabel_486["justify"] = "left"
    GLabel_486["text"] = ""
    GLabel_486.place(x=360, y=40, width=120, height=40)

    return frame

def create_page2():
    frame = tk.Frame(container)
    frame.grid(row=0, column=0, sticky="nsew")
    label = tk.Label(frame, text="Collect Data:")
    label.pack(side="top", fill="x", pady=10)
    return frame

def create_page3():
    frame = tk.Frame(container)
    frame.grid(row=0, column=0, sticky="nsew")
    label = tk.Label(frame, text="ML Model Training:")
    label.pack(side="top", fill="x", pady=10)
    return frame

def create_page4():
    frame = tk.Frame(container)
    frame.grid(row=0, column=0, sticky="nsew")
    label = tk.Label(frame, text="Visualizing Data:")
    label.pack(side="top", fill="x", pady=10)
    return frame

frames["Page1"] = create_page1()
frames["Page2"] = create_page2()
frames["Page3"] = create_page3()
frames["Page4"] = create_page4()

# Show the first page by default
show_frame("Page1")

# Navigation bar
nav_frame = tk.Frame(root)
nav_frame.pack(anchor="nw", padx=10, pady=10)

for page_name in frames:
    button = tk.Button(nav_frame, text=page_name, command=lambda name=page_name: show_frame(name))
    button.pack(side="left", padx=5)

root.mainloop()
