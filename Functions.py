import serial.tools.list_ports as list_ports
import matplotlib.pyplot as plt
import serial
import os
import shutil

# default values for the serial communication
port = "COM3"
baud_rate = 9600

# flags for the selection of port and baud rate
is_training_finished = False
is_port_selected = False
is_baud_rate_selected = False


# this function returns a list of available ports
def get_ports():
    ports_available = list_ports.comports()
    ports = []
    for i in ports_available:
        ports.append([i.device, i.description])
    return ports


# this function gives available baud rates for the serial communication
def get_baudRates():
    return [9600, 19200, 38400, 57600, 115200]


# this function updates the same graph with new data refresh time is given as a parameter
def update_graph(x, y, refresh_time):
    plt.plot(x, y)
    plt.pause(refresh_time)
    plt.show()


# this function reads all the data come from serial port to blank text file "training_data.txt"
# and this same function look for file size of the training data until it get 1MB then it stop the reading
def read_data():
    ser = serial.Serial(port, baud_rate)
    ser.flushInput()
    ser.flushOutput()
    ser.flush()
    file = open("training_data.txt", "w")
    file_size = 0
    while file_size < 1000000:
        data = ser.readline()
        file.write(data)
        file_size += len(data)
    file.close()
    ser.close()


# this is a anomaly detection function which is a machine learning model trained by the data in "training_data.txt"
def anomaly_detection(data_point):
    return 1


# this function reads the data in Machine_List.txt file and return the list of machine names
def Machine_List():
    # open the "Machines.txt" file and read the machine names
    file = open("Machines.txt", "r")
    machines = file.readlines()
    file.close()
    return [machine.strip().strip('\n') for machine in machines]

# this function adds a new machine name to the "Machines.txt" file
def add_machine(machine_name):
    file = open("Machines.txt", "a")
    file.write(machine_name + '\n')
    file.close()

# this function deletes the machine name from the "Machines.txt" file
def delete_machine(machine_name):
    file = open("Machines.txt", "r")
    machines = file.readlines()
    file.close()
    file = open("Machines.txt", "w")
    for machine in machines:
        if machine.strip().strip('\n') != machine_name:
            file.write(machine)
    file.close()

# for machine in Machine_List() create seperate folder in the directory
# inside every folder create 2 txt files called "Train_Data.txt" and "Test_Data.txt"
# def create_folders():
#     for machine in Machine_List():
#         machine = machine.strip().strip('\n')
#         try:
#             os.mkdir(machine)
#             file = open(machine + f"/{machine}_Train_Data.txt", "w")
#             file.close()
#             file = open(machine + f"/{machine}_Test_Data.txt", "w")
#             file.close()
#         except FileExistsError:
#             pass

# create a folder for the machine with the machine name and create 2 txt files inside the folder called "Train_Data.txt" and "Test_Data.txt"
def create_a_folder(machine_name):
    try:
        os.mkdir(machine_name)
        file = open(machine_name + f"/{machine_name}_Train_Data.txt", "w")
        file.close()
        file = open(machine_name + f"/{machine_name}_Test_Data.txt", "w")
        file.close()
    except FileExistsError:
        pass


# delete the folder of the selected machine with all the items inside it
def deleteMachineFolder(machine_name):
    try:
        shutil.rmtree(machine_name)
    except FileNotFoundError:
        pass

# print(Machine_List())
# create_folders()

# when the parth to a txt file is given find the file size in Kb
def get_file_size(file_path):
    file = open(file_path, "r")
    file_size = os.path.getsize(file_path)
    file.close()
    return file_size / 1024


# validate machine name before adding it to the Machines.txt file and before create new files for the machine
def validate_machine_name(machine_name):
    if machine_name in Machine_List():
        return [False, "Machine name already exists"]
    elif machine_name == "":
        return [False, "Machine name cannot be empty"]
    else:
        return [True, "Machine name is valid"]

