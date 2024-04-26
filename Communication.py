import serial
import serial.tools.list_ports


def find_arduino(port=None):
    """Get the name of the port that is connected to Arduino."""
    if port is None:
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if p.manufacturer is not None and "Microsoft" in p.manufacturer:
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
            ser.open()
            if ser.is_open:
                # print("Serial port: " + port + " is opened.")
                return ser
            else:
                # print("Serial port: " + port + " cannot be opened.")
                return None
        except serial.SerialException as e:
            # print("Serial port: " + port + " cannot be opened.")
            # print(e)
            return None
    return ser


port_ = find_arduino()
ser_ = get_serial_port(port_, 115200)
