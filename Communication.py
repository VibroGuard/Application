import serial
import serial.tools.list_ports


def find_arduino(port=None):
    """Get the name of the port that is connected to Arduino."""
    if port is None:
        ports = serial.tools.list_ports.comports()
        for p in ports:
            # print(p.manufacturer)
            if p.manufacturer is not None and ("Arduino" in p.manufacturer or "FTDI" in p.manufacturer):
                port = p.device
    return port


def get_serial_port(port=None, baudrate=115200):
    ser = None

    if port is None:
        port = find_arduino()

    if port is not None:
        ser = serial.Serial()
        ser.baudrate = baudrate
        ser.port = port

        try:
            if not ser.is_open:
                ser.open()
            if ser.is_open:
                print("Serial port: " + port + " is opened.")
                return ser
            else:
                # print("Serial port: " + port + " cannot be opened.")
                return None
        except serial.SerialException as e:
            # print("Serial port: " + port + " cannot be opened.")
            # print(e)
            return None
    return None


# port_ = find_arduino()
# ser_ = get_serial_port(port_, 115200)
#
# print("Port: ", port_)
# print("Serial port: ", ser_)

def ComOK():
    port_ = find_arduino()
    ser_ = get_serial_port(port_, 115200)

    if ser_ is not None:
        return [ser_, ser_.isOpen(), ser_.port, ser_.baudrate]
    else:
        return [ser_, False, "ComPort?", "Baudrate?"]

# print(ComOK())
