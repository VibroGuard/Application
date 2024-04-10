import serial.tools.list_ports as list_ports
import matplotlib.pyplot as plt
import serial

port = "COM3"
baud_rate = 9600

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


