import tkinter as tk
import tkinter.font as tkFont
from Functions import *


def GButton_295_command():
    print("command")


def GButton_910_command():
    print("command")


def GButton_536_command():
    print("command")


def GButton_638_command():
    # print("command")
    machine_name = GLineEdit_334.get()
    validation = validate_machine_name(machine_name)
    if validation[0]:
        print(validation[1])
        print(Machine_List())
        add_machine(machine_name)           # add the machine name to the Machines.txt file
        print(Machine_List())
        create_a_folder(machine_name)         # create a folder for the machine
        GListBox_969.insert(tk.END, machine_name)       # add the machine name to the list box
        GLineEdit_334.delete(0, tk.END)        # clear the entry box
    else:
        print(validation[1])


def GButton_450_command():
    deleting_machine = GListBox_969.curselection()
    if deleting_machine:
        selected_index = deleting_machine[0]  # Assuming single selection
        selected_value = GListBox_969.get(selected_index)
        print("Selected value:", selected_value)
        deleteMachineFolder(selected_value)        # delete the folder of the selected machine
        GListBox_969.delete(selected_index)          # delete the selected machine from the list box
        delete_machine(selected_value)          # delete the selected machine from the Machines.txt file
    else:
        print("No item selected.")


root = tk.Tk()
root.title("VIBROGUARD")
width = 800
height = 600
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignStr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
root.geometry(alignStr)

# select communication label
GLabel_421 = tk.Label(root)
GLabel_421["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
GLabel_421["font"] = ft
GLabel_421["fg"] = "#434343"
GLabel_421["justify"] = "center"
GLabel_421["text"] = "Select Communication"
GLabel_421.place(x=40, y=40, width=128, height=30)

# select com port label
GLabel_871 = tk.Label(root)
GLabel_871["anchor"] = "center"
GLabel_871["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
GLabel_871["font"] = ft
GLabel_871["fg"] = "#333333"
GLabel_871["justify"] = "center"
GLabel_871["text"] = "Select COM Port"
GLabel_871.place(x=40, y=80, width=99, height=30)

# select baud rate label
GLabel_791 = tk.Label(root)
GLabel_791["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
GLabel_791["font"] = ft
GLabel_791["fg"] = "#333333"
GLabel_791["justify"] = "center"
GLabel_791["text"] = "Select Baud Rate"
GLabel_791.place(x=210, y=80, width=109, height=30)

# ok button for com port and baud rate selection
GButton_295 = tk.Button(root)
GButton_295["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times', size=10)
GButton_295["font"] = ft
GButton_295["fg"] = "#000000"
GButton_295["justify"] = "center"
GButton_295["text"] = "OK"
GButton_295.place(x=390, y=80, width=60, height=30)
GButton_295["command"] = GButton_295_command

# list box for selecting the port
GListBox_108 = tk.Listbox(root)
GListBox_108["borderwidth"] = "1px"
ft = tkFont.Font(family='Times', size=10)
GListBox_108["font"] = ft
GListBox_108["fg"] = "#333333"
GListBox_108["justify"] = "center"
GListBox_108.place(x=40, y=120, width=79, height=102)

# list box for selecting the baud rate
GListBox_600 = tk.Listbox(root)
GListBox_600["borderwidth"] = "1px"
ft = tkFont.Font(family='Times', size=10)
GListBox_600["font"] = ft
GListBox_600["fg"] = "#333333"
GListBox_600["justify"] = "center"
GListBox_600.place(x=210, y=120, width=77, height=99)
baud_rate_list = get_baudRates()
for baudRate in baud_rate_list:
    GListBox_600.insert(tk.END, baudRate)

# select machine label
GLabel_454 = tk.Label(root)
GLabel_454["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
GLabel_454["font"] = ft
GLabel_454["fg"] = "#333333"
GLabel_454["justify"] = "center"
GLabel_454["text"] = "Select Machine"
GLabel_454.place(x=40, y=280, width=90, height=31)

# select the machine label
GLabel_150 = tk.Label(root)
GLabel_150["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
GLabel_150["font"] = ft
GLabel_150["fg"] = "#333333"
GLabel_150["justify"] = "center"
GLabel_150["text"] = "Select The  Machine"
GLabel_150.place(x=40, y=320, width=124, height=38)

# train button
GButton_910 = tk.Button(root)
GButton_910["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times', size=10)
GButton_910["font"] = ft
GButton_910["fg"] = "#000000"
GButton_910["justify"] = "center"
GButton_910["text"] = "TRAIN"
GButton_910.place(x=390, y=320, width=60, height=30)
GButton_910["command"] = GButton_910_command

# visualize button
GButton_536 = tk.Button(root)
GButton_536["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times', size=10)
GButton_536["font"] = ft
GButton_536["fg"] = "#000000"
GButton_536["justify"] = "center"
GButton_536["text"] = "VISUALIZE"
GButton_536.place(x=470, y=320, width=68, height=30)
GButton_536["command"] = GButton_536_command

# list box for selecting the machine
GListBox_969 = tk.Listbox(root)
GListBox_969["borderwidth"] = "1px"
ft = tkFont.Font(family='Times', size=10)
GListBox_969["font"] = ft
GListBox_969["fg"] = "#333333"
GListBox_969["justify"] = "center"
GListBox_969.place(x=40, y=370, width=79, height=111)
machine_list = Machine_List()
for machine in machine_list:
    GListBox_969.insert(tk.END, machine)

# add new machine label
GLabel_540 = tk.Label(root)
GLabel_540["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
GLabel_540["font"] = ft
GLabel_540["fg"] = "#333333"
GLabel_540["justify"] = "center"
GLabel_540["text"] = "Add New Machine"
GLabel_540.place(x=210, y=320, width=118, height=40)

# enter new machine name
GLineEdit_334 = tk.Entry(root)
GLineEdit_334["borderwidth"] = "1px"
ft = tkFont.Font(family='Times', size=10)
GLineEdit_334["font"] = ft
GLineEdit_334["fg"] = "#333333"
GLineEdit_334["justify"] = "center"
GLineEdit_334["text"] = "Enter Name Here"
GLineEdit_334.place(x=210, y=370, width=116, height=30)

# ok button for adding new machine
GButton_638 = tk.Button(root)
GButton_638["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times', size=10)
GButton_638["font"] = ft
GButton_638["fg"] = "#000000"
GButton_638["justify"] = "center"
GButton_638["text"] = "OK"
GButton_638.place(x=210, y=410, width=62, height=30)
GButton_638["command"] = GButton_638_command

GButton_450 = tk.Button(root)
GButton_450["bg"] = "#f0f0f0"
ft = tkFont.Font(family='Times', size=10)
GButton_450["font"] = ft
GButton_450["fg"] = "#000000"
GButton_450["justify"] = "center"
GButton_450["text"] = "Delete"
GButton_450.place(x=210, y=500, width=62, height=30)
GButton_450["command"] = GButton_450_command

GLabel_445 = tk.Label(root)
GLabel_445["bg"] = "#ffffff"
ft = tkFont.Font(family='Times', size=10)
GLabel_445["font"] = ft
GLabel_445["fg"] = "#333333"
GLabel_445["justify"] = "center"
GLabel_445["text"] = "Delete Machine"
GLabel_445.place(x=210, y=450, width=101, height=44)


root.mainloop()
