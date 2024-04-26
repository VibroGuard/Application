import serial.tools.list_ports as list_ports
import matplotlib.pyplot as plt
import serial
import os
import shutil
import serial.tools.list_ports

# this function gives the data availabled methods to train
def Data_Collection_Method():
    return ["NewData", "LoadFromFile"]


# this function updates the same graph with new data refresh time is given as a parameter
def update_graph(x, y, refresh_time):
    plt.plot(x, y)
    plt.pause(refresh_time)
    plt.show()


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
        file = open(machine_name + f"/{machine_name}_Model.txt", "w")
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
        return [False, "Machine name already exists. Enter valid machine name"]
    elif machine_name == "":
        return [False, "Machine name cannot be empty. Enter valid machine name"]
    else:
        return [True, "New Machine is added"]