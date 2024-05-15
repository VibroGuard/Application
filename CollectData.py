import time
import numpy as np
import os

def fill_buffer(num_samples, ser):
    i = 0
    temp_buffer = []
    temp_buffer.clear()

    while i < num_samples:
        try:
            value = float(ser.readline())
        except:
            value = 0.0
        # print("value: ", value)

        temp_buffer.append(value)
        i += 1

    # return np.array(temp_buffer).reshape(-1, 1)
    return temp_buffer


def collect_dataset(samples_amount, time_amount, num_samples, ser, DataSetFolderPath):
    start_time = time.time()
    samples = 0

    x_data_buffer = []
    y_data_buffer = []
    z_data_buffer = []

    x_data_buffer.clear()
    y_data_buffer.clear()
    z_data_buffer.clear()

    with open(f"{DataSetFolderPath}/x_data.txt", "wt"):
        pass
    with open(f"{DataSetFolderPath}/y_data.txt", "wt"):
        pass
    with open(f"{DataSetFolderPath}/z_data.txt", "wt"):
        pass

    while (time.time() - start_time <= time_amount) and (samples < samples_amount):
        print(time.time() - start_time)
        print(samples)

        received_data = str(ser.readline())

        if "x" in received_data:
            x_data = fill_buffer(num_samples, ser)
            x_data_buffer.extend(x_data)
            with open(f"{DataSetFolderPath}/x_data.txt", "at") as x_data_file:
                for x in x_data:
                    x_data_file.write(str(x))
                    x_data_file.write(" ")

            # Increment the samples count.
            samples += num_samples
        elif "y" in received_data and samples != 0:
            y_data = fill_buffer(num_samples, ser)
            y_data_buffer.extend(y_data)
            with open(f"{DataSetFolderPath}/y_data.txt", "at") as y_data_file:
                for y in y_data:
                    y_data_file.write(str(y))
                    y_data_file.write(" ")
        elif "z" in received_data and samples != 0:
            z_data = fill_buffer(num_samples, ser)
            z_data_buffer.extend(z_data)
            with open(f"{DataSetFolderPath}/z_data.txt", "at") as z_data_file:
                for z in z_data:
                    z_data_file.write(str(z))
                    z_data_file.write(" ")

    return np.array(x_data_buffer).reshape(-1, 1), np.array(y_data_buffer).reshape(-1, 1), np.array(
        z_data_buffer).reshape(-1, 1)

