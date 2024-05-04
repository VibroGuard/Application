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


# message types are Information Warning and Error
def show_message(Mtype, message):
    if Mtype == "Information":
        messagebox.showinfo(Mtype, message)
    elif Mtype == "Warning":
        messagebox.showwarning(Mtype, message)
    elif Mtype == "Error":
        messagebox.showerror(Mtype, message)
    else:
        print("Invalid message type")


def get_method():
    selected_indices = GListBox_600.curselection()
    selected_values = [GListBox_600.get(index) for index in selected_indices]
    return selected_values


def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    GLabel_489.config(text=current_time)
    # Update time every 1000 milliseconds (1 second)
    root.after(1000, update_time)


# start communication button
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


def GButton_910_command():
    show_message("Information", "Make sure not to unplug device while training \nThe default method is LoadFromFIle")
    show_message("Information", "'Start Communication' button should be clicked before training")
    method = get_method()
    print(method)
    try:
        if method[0] == "LoadFromFile" or method is None:
            x_data_buffer, y_data_buffer, z_data_buffer = collect_dataset(2000, 10, 512, ser_)
            with Pool() as pool:
                trained_models = pool.map(model, (x_data_buffer, y_data_buffer, z_data_buffer))

        else:
            x_data = np.loadtxt("x_data.txt").reshape(-1, 1)
            y_data = np.loadtxt("y_data.txt").reshape(-1, 1)
            z_data = np.loadtxt("z_data.txt").reshape(-1, 1)
            with Pool() as pool:
                trained_models = pool.map(model, (x_data, y_data, z_data))
    except:
        show_message("Error", "Cannot Train! make sure your plugged and pressed 'start communication' button'")


def GButton_536_command():
    print("Entered...")
    show_message("Information", "'Start Communication' button should be clicked before visualizing")
    try:
        num_samples = 512
        sampling_frequency = 250

        x_data = [0.0] * num_samples
        y_data = [0.0] * num_samples
        z_data = [0.0] * num_samples

        fig, axs = plt.subplots(2, 3, figsize=(15, 5))
        while True:
            print("Entered while loop...")
            received_data = str(ser_.readline())[2:-5].casefold()
            print("Received: ", received_data)

            if received_data == "x":
                x_data = fill_buffer(num_samples, ser_)
            elif received_data == "y":
                y_data = fill_buffer(num_samples, ser_)
            elif received_data == "z":
                z_data = fill_buffer(num_samples, ser_)
            else:
                continue

            # x_data, y_data, z_data = get_new_dataset(ser, num_samples)
            print(x_data)
            print(y_data)
            print(z_data)
            print("Visualizing...")
            visualize_data(x_data, y_data, z_data, sampling_frequency, "time", fig, axs)
    except:
        show_message("Error", "Cannot Visualize! make sure your plugged and pressed 'start communication' button'")

# format the data size and time to integer
def format_data(data):
    try:
        return int(data)
    except:
        return None


# return size of data to be collected
def getDataSize():
    return format_data(GLineEdit_334.get())


# return time of data to be collected
def getTime():
    return format_data(GLineEdit_335.get())


def GButton_537_command():
    show_message("Information", "'Start Communication' button should be clicked before visualizing")
    global x
    try:
        print(getDataSize())
        print(getTime())
        x = collect_dataset(20000, 10, 512, ser_)
    except:
        show_message("Error", "Cannot collect data! make sure your plugged")





# this function validates the machine name
# def GButton_638_command():
#     # print("command")
#     machine_name = GLineEdit_334.get()
#     validation = validate_machine_name(machine_name)
#     if validation[0]:
#         print(validation[1])
#         show_message("Information", validation[1])
#         print(Machine_List())
#         add_machine(machine_name)  # add the machine name to the Machines.txt file
#         print(Machine_List())
#         create_a_folder(machine_name)  # create a folder for the machine
#         GListBox_969.insert(tk.END, machine_name)  # add the machine name to the list box
#         GLineEdit_334.delete(0, tk.END)  # clear the entry box
#     else:
#         print(validation[1])
#         show_message("Error", validation[1])


# this function deletes the selected machine from the list box and the Machines.txt file
# def GButton_450_command():
#     deleting_machine = GListBox_969.curselection()
#     if deleting_machine:
#         selected_index = deleting_machine[0]  # Assuming single selection
#         selected_value = GListBox_969.get(selected_index)
#         print("Selected value:", selected_value)
#         deleteMachineFolder(selected_value)  # delete the folder of the selected machine
#         GListBox_969.delete(selected_index)  # delete the selected machine from the list box
#         delete_machine(selected_value)  # delete the selected machine from the Machines.txt file
#     else:
#         print("No item selected.")
#         show_message("Error", "No item selected.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("VIBROGUARD")
    width = 800
    height = 600
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    alignStr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(alignStr)

    # Start communication button
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

    # data
    GLabel_791 = tk.Label(root)
    GLabel_791["bg"] = "#ffffff"
    ft = tkFont.Font(family='Times', size=10)
    GLabel_791["font"] = ft
    GLabel_791["fg"] = "#333333"
    GLabel_791["justify"] = "center"
    GLabel_791["text"] = "Load Data From?"
    GLabel_791.place(x=40, y=100, width=120, height=40)

    GListBox_600 = tk.Listbox(root)
    GListBox_600["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=10)
    GListBox_600["font"] = ft
    GListBox_600["fg"] = "#333333"
    GListBox_600["justify"] = "left"
    GListBox_600.place(x=40, y=160, width=100, height=100)
    # data_collect_method_list = Data_Collection_Method()
    # for dataMethod in data_collect_method_list:
    #     GListBox_600.insert(tk.END, dataMethod)

    # ML model
    GLabel_792 = tk.Label(root)
    GLabel_792["bg"] = "#ffffff"
    ft = tkFont.Font(family='Times', size=10)
    GLabel_792["font"] = ft
    GLabel_792["fg"] = "#333333"
    GLabel_792["justify"] = "center"
    GLabel_792["text"] = "Load ML model from?"
    GLabel_792.place(x=200, y=100, width=120, height=40)

    GListBox_601 = tk.Listbox(root)
    GListBox_601["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=10)
    GListBox_601["font"] = ft
    GListBox_601["fg"] = "#333333"
    GListBox_601["justify"] = "left"
    GListBox_601.place(x=200, y=160, width=100, height=100)
    # data_collect_method_list = Data_Collection_Method()
    # for dataMethod in data_collect_method_list:
    #     GListBox_601.insert(tk.END, dataMethod)

    # train button
    GButton_910 = tk.Button(root)
    GButton_910["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    GButton_910["font"] = ft
    GButton_910["fg"] = "#000000"
    GButton_910["justify"] = "center"
    GButton_910["text"] = "TRAIN"
    GButton_910.place(x=40, y=340, width=120, height=40)
    GButton_910["command"] = GButton_910_command

    # visualize button
    GButton_536 = tk.Button(root)
    GButton_536["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    GButton_536["font"] = ft
    GButton_536["fg"] = "#000000"
    GButton_536["justify"] = "center"
    GButton_536["text"] = "VISUALIZE"
    GButton_536.place(x=40, y=400, width=120, height=40)
    GButton_536["command"] = GButton_536_command

    # visualize button
    GButton_537 = tk.Button(root)
    GButton_537["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    GButton_537["font"] = ft
    GButton_537["fg"] = "#000000"
    GButton_537["justify"] = "center"
    GButton_537["text"] = "COLLECT DATA"
    GButton_537.place(x=360, y=280, width=120, height=40)
    GButton_537["command"] = GButton_537_command

    # get collect data size
    GLineEdit_334 = tk.Entry(root)
    GLineEdit_334["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=10)
    GLineEdit_334["font"] = ft
    GLineEdit_334["fg"] = "#333333"
    GLineEdit_334["justify"] = "center"
    GLineEdit_334.insert(0, "choose (KB) Default: 1KB")
    GLineEdit_334.place(x=40, y=280, width=120, height=40)

    # get collect data time
    GLineEdit_335 = tk.Entry(root)
    GLineEdit_335["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=10)
    GLineEdit_335["font"] = ft
    GLineEdit_335["fg"] = "#333333"
    GLineEdit_335["justify"] = "center"
    GLineEdit_335.insert(0, "choose (min) Default: 10min")
    GLineEdit_335.place(x=200, y=280, width=120, height=40)

    GLabel_489 = tk.Label(root)
    GLabel_489["bg"] = "#ffffff"
    ft = tkFont.Font(family='Times', size=10)
    GLabel_489["font"] = ft
    GLabel_489["fg"] = "#333333"
    GLabel_489["justify"] = "center"
    GLabel_489["text"] = ""
    GLabel_489.place(x=650, y=550, width=110, height=30)

    update_time()

    root.mainloop()
