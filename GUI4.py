import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from datetime import datetime
from Communication import *
from CollectData import collect_dataset, fill_buffer


# if data is given as a string, extract the integer from it, remove white spaces
# and string parts, and convert it to an integer
def format_data(data):
    return int(''.join(filter(str.isdigit, data)))


def show_message(Mtype, message):
    if Mtype == "Information":
        messagebox.showinfo(Mtype, message)
    elif Mtype == "Warning":
        messagebox.showwarning(Mtype, message)
    elif Mtype == "Error":
        messagebox.showerror(Mtype, message)
    else:
        print("Invalid message type")


def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    timeLabel.config(text=current_time)
    root.after(1000, update_time)


def serialConnect_Command():
    status = ComOK()
    print(status)
    # ser_obj = status[0]
    ok = status[1]
    port = status[2]
    baudRate = status[3]
    print(ok, port, baudRate)
    if ok:
        portLabel.config(text=port)
        baudRateLabel.config(text=baudRate)
        show_message("Information", f"Port - {port} with baud rate - {baudRate} is ready")
    else:
        portLabel.config(text=port)
        baudRateLabel.config(text=baudRate)
        show_message("Error", "No port found")


def collectData_command():
    time = getTime()
    size = getDataSize()
    serObj = ComOK()[0]
    show_message("Information", "'Start Communication' button should be clicked before visualizing")
    try:
        print(getDataSize())
        print(getTime())
        x = collect_dataset(20000, time, size, serObj)
    except:
        show_message("Error", "Cannot collect data! make sure you're plugged")


def getDataSize():
    return format_data(getDataSizeEntry.get())


def getTime():
    return format_data(getTimeEntry.get())


def show_select_com_port_window():
    select_com_port_frame.tkraise()


def show_collect_data_window():
    collect_data_frame.tkraise()


def show_train_ml_model_window():
    train_ml_model_frame.tkraise()


def show_visualize_data_window():
    visualize_data_frame.tkraise()


root = tk.Tk()
root.geometry("400x300")
root.title("VIBROGUARD")
root.resizable(False, False)

# Main frame to contain pages
# main_frame = tk.Frame(root)
# main_frame.pack(fill=tk.BOTH, expand=True)

# Select COM Port Frame
select_com_port_frame = tk.Frame()
select_com_port_frame.pack(fill=tk.BOTH, expand=True)

serialConnectButton = tk.Button(select_com_port_frame)
serialConnectButton["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times', size=10)
serialConnectButton["font"] = ft
serialConnectButton["fg"] = "#000000"
serialConnectButton["justify"] = "center"
serialConnectButton["text"] = "Start Communication"
serialConnectButton.place(x=40, y=40, width=120, height=40)
serialConnectButton["command"] = serialConnect_Command

# port label
portLabel = tk.Label(select_com_port_frame)
portLabel["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
portLabel["font"] = ft
portLabel["fg"] = "#333333"
portLabel["justify"] = "left"
portLabel["text"] = ""
portLabel.place(x=40, y=100, width=120, height=40)

# baud rate label
baudRateLabel = tk.Label(select_com_port_frame)
baudRateLabel["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
baudRateLabel["font"] = ft
baudRateLabel["fg"] = "#333333"
baudRateLabel["justify"] = "left"
baudRateLabel["text"] = ""
baudRateLabel.place(x=40, y=160, width=120, height=40)

# Collect Data Frame
collect_data_frame = tk.Frame(root)
collect_data_frame.pack(fill=tk.BOTH, expand=True)

# collect Data Button
collectDataButton = tk.Button(collect_data_frame)
collectDataButton["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times', size=10)
collectDataButton["font"] = ft
collectDataButton["fg"] = "#000000"
collectDataButton["justify"] = "center"
collectDataButton["text"] = "COLLECT DATA"
collectDataButton.place(x=40, y=40, width=120, height=40)
collectDataButton["command"] = collectData_command

# get collect data size label
getDataSizeLabel = tk.Label(collect_data_frame)
getDataSizeLabel["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
getDataSizeLabel["font"] = ft
getDataSizeLabel["fg"] = "#333333"
getDataSizeLabel["justify"] = "left"
getDataSizeLabel["text"] = "Data Size: give in KB"
getDataSizeLabel.place(x=200, y=100, width=200, height=40)

# get collect data size
getDataSizeEntry = tk.Entry(collect_data_frame)
getDataSizeEntry["borderwidth"] = "1px"
ft = tkFont.Font(family='Times', size=10)
getDataSizeEntry["font"] = ft
getDataSizeEntry["fg"] = "#333333"
getDataSizeEntry["justify"] = "center"
getDataSizeEntry.insert(0, "1KB")
getDataSizeEntry.place(x=40, y=100, width=120, height=40)

# get collect data time label
getTimeLabel = tk.Label(collect_data_frame)
getTimeLabel["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
getTimeLabel["font"] = ft
getTimeLabel["fg"] = "#333333"
getTimeLabel["justify"] = "left"
getTimeLabel["text"] = "Time: give in min"
getTimeLabel.place(x=200, y=160, width=200, height=40)

# get collect data time
getTimeEntry = tk.Entry(collect_data_frame)
getTimeEntry["borderwidth"] = "1px"
ft = tkFont.Font(family='Times', size=10)
getTimeEntry["font"] = ft
getTimeEntry["fg"] = "#333333"
getTimeEntry["justify"] = "center"
getTimeEntry.insert(0, "10min")
getTimeEntry.place(x=40, y=160, width=120, height=40)

# Train ML Model Frame
train_ml_model_frame = tk.Frame(root)
train_ml_model_frame.pack(fill=tk.BOTH, expand=True)

# Visualize Data Frame
visualize_data_frame = tk.Frame(root)
visualize_data_frame.pack(fill=tk.BOTH, expand=True)

# Buttons to switch between frames
select_com_port_button = tk.Button(root, text="Select COM Port", command=show_select_com_port_window, width=20,
                                   height=2)
select_com_port_button.pack(pady=10)

collect_data_button = tk.Button(root, text="Collect Data", command=show_collect_data_window, width=20, height=2)
collect_data_button.pack(pady=10)

train_ml_model_button = tk.Button(root, text="Train ML Model", command=show_train_ml_model_window, width=20,
                                  height=2)
train_ml_model_button.pack(pady=10)

visualize_data_button = tk.Button(root, text="Visualize Data", command=show_visualize_data_window, width=20,
                                  height=2)
visualize_data_button.pack(pady=10)

timeLabel = tk.Label(root)
timeLabel["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
timeLabel["font"] = ft
timeLabel["fg"] = "#333333"
timeLabel["justify"] = "center"
timeLabel["text"] = ""
timeLabel.place(x=290, y=250, width=110, height=30)

update_time()

root.mainloop()
