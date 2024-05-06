import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox

import joblib

from Communication import ComOK
from CollectData import collect_dataset, fill_buffer
from datetime import datetime
from multiprocessing import Pool
from Graphs import *
from ML import model, predict
from keras.models import load_model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

datasize_Main = 256

defaultNumberOfSamples = 20000
defaultDataTime = 100
sampling_frequency = 200


# find whether content available in a file when given the file name
def find_content(file_name):
    try:
        with open(file_name, "r") as file:
            content = file.read()
            if content:
                return True
            else:
                return False
    except FileNotFoundError:
        return False


def update_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    showTimeLabel.config(text=current_time)
    # Update time every 1000 milliseconds (1 second)
    root.after(1000, update_time)


def show_message(Mtype, message):
    if Mtype == "Information":
        messagebox.showinfo(Mtype, message)
    elif Mtype == "Warning":
        messagebox.showwarning(Mtype, message)
    elif Mtype == "Error":
        messagebox.showerror(Mtype, message)
    else:
        print("Invalid message type")


def Select_COM_Port_Page():
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
            show_message("Information", f"Port - {port} with baud rate - {baudRate} is ready.")
        else:
            portLabel.config(text=port)
            baudRateLabel.config(text=baudRate)
            show_message("Error", "No port found.")

    Select_COM_Port_Frame = tk.Frame(main_frame)

    # button to start communication
    serialConnectButton = tk.Button(main_frame)
    serialConnectButton["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    serialConnectButton["font"] = ft
    serialConnectButton["fg"] = "#000000"
    serialConnectButton["justify"] = "center"
    serialConnectButton["text"] = "Start Communication"
    serialConnectButton.place(x=20, y=50, width=150, height=40)
    serialConnectButton["command"] = serialConnect_Command

    # port label
    portLabel = tk.Label(main_frame)
    portLabel["bg"] = "#ffffff"
    ft = tkFont.Font(family='Times', size=10)
    portLabel["font"] = ft
    portLabel["fg"] = "#333333"
    portLabel["justify"] = "left"
    portLabel["text"] = ""
    portLabel.place(x=20, y=120, width=150, height=40)

    # baud rate label
    baudRateLabel = tk.Label(main_frame)
    baudRateLabel["bg"] = "#ffffff"
    ft = tkFont.Font(family='Times', size=10)
    baudRateLabel["font"] = ft
    baudRateLabel["fg"] = "#333333"
    baudRateLabel["justify"] = "left"
    baudRateLabel["text"] = ""
    baudRateLabel.place(x=20, y=190, width=150, height=40)

    Select_COM_Port_Frame.pack(pady=20)


def Collect_Data_Page():
    def format_data(data):
        return int(''.join(filter(str.isdigit, data)))

    def collectData_command():
        serObj = ComOK()[0]
        if serObj is None:
            show_message("Error", "Cannot collect data!\nPlug the Device!\nStart Communication First!")
        else:
            try:
                numOfSamples = getNumOfSamples()
                dataTime = getTime()
                x = collect_dataset(numOfSamples, dataTime, datasize_Main, serObj)
                print("from entries", numOfSamples, dataTime)
                print("defaultNumberOfSamples", defaultNumberOfSamples, "defaultDataTime", defaultDataTime)
            except:
                show_message("Error", "Cannot collect data!\nPlug the Device!\nStart Communication First!")
        # print("Collect Data")

    # return size of data to be collected
    def getNumOfSamples():
        global defaultNumberOfSamples
        defaultNumberOfSamples = format_data(getNumOfSamplesEntry.get())
        return defaultNumberOfSamples

    # return time of data to be collected
    def getTime():
        global defaultDataTime
        defaultDataTime = format_data(getTimeEntry.get())
        return defaultDataTime

    Collect_Data_Frame = tk.Frame(main_frame)

    # collect Data Button
    collectDataButton = tk.Button(main_frame)
    collectDataButton["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    collectDataButton["font"] = ft
    collectDataButton["fg"] = "#000000"
    collectDataButton["justify"] = "center"
    collectDataButton["text"] = "Collect Data"
    collectDataButton.place(x=20, y=50, width=150, height=40)
    collectDataButton["command"] = collectData_command

    # get collect data size label
    getDataSizeLabel = tk.Label(main_frame)
    getDataSizeLabel["bg"] = "#ffffff"
    ft = tkFont.Font(family='Times', size=10)
    getDataSizeLabel["font"] = ft
    getDataSizeLabel["fg"] = "#333333"
    getDataSizeLabel["justify"] = "left"
    getDataSizeLabel["text"] = "Give Number Of Samples: \nas an integer"
    getDataSizeLabel.place(x=200, y=120, width=150, height=40)

    # get collect data size
    global defaultNumberOfSamples
    getNumOfSamplesEntry = tk.Entry(main_frame)
    getNumOfSamplesEntry["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=10)
    getNumOfSamplesEntry["font"] = ft
    getNumOfSamplesEntry["fg"] = "#333333"
    getNumOfSamplesEntry["justify"] = "center"
    getNumOfSamplesEntry.insert(0, f"{str(defaultNumberOfSamples)}samples")
    getNumOfSamplesEntry.place(x=20, y=120, width=150, height=40)

    # get collect data time label
    global defaultDataTime
    getTimeLabel = tk.Label(main_frame)
    getTimeLabel["bg"] = "#ffffff"
    ft = tkFont.Font(family='Times', size=10)
    getTimeLabel["font"] = ft
    getTimeLabel["fg"] = "#333333"
    getTimeLabel["justify"] = "left"
    getTimeLabel["text"] = "Time: give in seconds"
    getTimeLabel.place(x=200, y=190, width=150, height=40)

    # get collect data time
    getTimeEntry = tk.Entry(main_frame)
    getTimeEntry["borderwidth"] = "1px"
    ft = tkFont.Font(family='Times', size=10)
    getTimeEntry["font"] = ft
    getTimeEntry["fg"] = "#333333"
    getTimeEntry["justify"] = "center"
    getTimeEntry.insert(0, f"{defaultDataTime}s")
    getTimeEntry.place(x=20, y=190, width=150, height=40)

    Collect_Data_Frame.pack(pady=20)


def Train_ML_Model_Page():
    Train_ML_Model_Frame = tk.Frame(main_frame)

    def Train_ML_New_Data():
        serObj = ComOK()[0]
        global trained_models
        if serObj is None:
            show_message("Error", "Cannot collect data!\nPlug the Device!\nStart Communication First!")
        else:
            if not serObj.isOpen():
                print("Opening ser port since it is closed.")
                serObj.open()

            YN = messagebox.askquestion("Question",
                                        f"Data collection started with \n{defaultNumberOfSamples} samples and {defaultDataTime} seconds.\nProceed?")
            if YN == "yes":
                # dataSet = collect_dataset(defaultNumberOfSamples, defaultDataTime, datasize_Main, serObj)

                # TEMPORARILY - To reduce time while debugging
                dataSet = collect_dataset(1000, defaultDataTime, datasize_Main, serObj)

                # store data in the file - Done in Collect_dataset function
                # train from stored data
                with Pool() as pool:
                    trained_models = pool.map(model, (dataSet[0], dataSet[1], dataSet[2]))

                # Store trained models
                trained_models[0][0].save("x_model.keras")
                trained_models[1][0].save("y_model.keras")
                trained_models[2][0].save("z_model.keras")

                # Storing fitted scalers
                joblib.dump(trained_models[0][2], "x_scaler.save")
                joblib.dump(trained_models[1][2], "y_scaler.save")
                joblib.dump(trained_models[2][2], "z_scaler.save")

                # Storing max_MAE values
                with open("x_maxMAE.txt", "wt") as x_maxMAE:
                    x_maxMAE.write(str(trained_models[0][1]))
                with open("y_maxMAE.txt", "wt") as y_maxMAE:
                    y_maxMAE.write(str(trained_models[1][1]))
                with open("z_maxMAE.txt", "wt") as z_maxMAE:
                    z_maxMAE.write(str(trained_models[2][1]))

                show_message("Information", "Model trained from new data.")
            else:
                show_message("Information",
                             "Data collection cancelled.\nGo to Collect Data page to set parameters.\n"
                             "Collect data on that page.\nCome here.\nClick on Train With Existing Data.")

    def Train_ML_Existing_Data():
        global trained_models
        # check Files does exist
        # train
        if find_content("x_data.txt") and find_content("y_data.txt") and find_content("z_data.txt"):
            # read 3 files
            # x
            # y
            # z
            # with Pool() as pool:
            #     trained_models = pool.map(model, (dataSet[0], dataSet[1], dataSet[2]))
            pass

        # Store trained models
        trained_models[0][0].save("x_model.keras")
        trained_models[1][0].save("y_model.keras")
        trained_models[2][0].save("z_model.keras")

        # Storing fitted scalers
        joblib.dump(trained_models[0][2], "x_scaler.save")
        joblib.dump(trained_models[1][2], "y_scaler.save")
        joblib.dump(trained_models[2][2], "z_scaler.save")

        # Storing max_MAE values
        with open("x_maxMAE.txt", "wt") as x_maxMAE:
            x_maxMAE.write(str(trained_models[0][1]))
        with open("y_maxMAE.txt", "wt") as y_maxMAE:
            y_maxMAE.write(str(trained_models[1][1]))
        with open("z_maxMAE.txt", "wt") as z_maxMAE:
            z_maxMAE.write(str(trained_models[2][1]))

        show_message("Information", "Model trained from existing data.")

    trainFromNewData = tk.Button(main_frame)
    trainFromNewData["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    trainFromNewData["font"] = ft
    trainFromNewData["fg"] = "#000000"
    trainFromNewData["justify"] = "center"
    trainFromNewData["text"] = "Train With New Data"
    trainFromNewData.place(x=20, y=50, width=200, height=40)
    trainFromNewData["command"] = Train_ML_New_Data

    trainFromExistingData = tk.Button(main_frame)
    trainFromExistingData["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    trainFromExistingData["font"] = ft
    trainFromExistingData["fg"] = "#000000"
    trainFromExistingData["justify"] = "center"
    trainFromExistingData["text"] = "Train With Existing Data"
    trainFromExistingData.place(x=20, y=120, width=200, height=40)
    trainFromExistingData["command"] = Train_ML_Existing_Data

    Train_ML_Model_Frame.pack(pady=20)


def Visualize_Data_Page():
    Visualize_Data_Frame = tk.Frame(main_frame)
    serObj = ComOK()[0]
    print("Ser object, ", serObj, serObj.isOpen())

    def on_close(event):
        print("Event: ", event)
        serObj.close()


    def Just_Visualize_Data():
        if serObj is None:
            show_message("Error", "Cannot collect data!\nPlug the Device!\nStart Communication First!")
        else:
            if not serObj.isOpen():
                print("Opening ser port since it is closed.")
                serObj.open()

            fig, axs = plt.subplots(1, 3, figsize=(5, 5))
            fig.canvas.mpl_connect('close_event', on_close)

            x_data = [0.0] * datasize_Main
            y_data = [0.0] * datasize_Main
            z_data = [0.0] * datasize_Main

            while True:
                print("In while True loop...")
                if not serObj.isOpen():
                    print("Breaking while loop...")
                    break
                else:
                    print("Continuing...")

                # Might be helpful to use a separate thread to run the while loop,
                # which will automatically terminate after the main program stops.
                print("Before receiving data")
                # received_data = str(serObj.readline())[2:-5].casefold()
                received_data = str(serObj.readline())
                print(received_data)

                # if received_data == "x":
                #     x_data = fill_buffer(datasize_Main, serObj)
                #     continue
                # elif received_data == "y":
                #     y_data = fill_buffer(datasize_Main, serObj)
                #     continue
                # elif received_data == "z":
                #     z_data = fill_buffer(datasize_Main, serObj)
                if "x" in received_data:
                    x_data = fill_buffer(datasize_Main, serObj)
                    continue
                elif "y" in received_data:
                    y_data = fill_buffer(datasize_Main, serObj)
                    continue
                elif "z" in received_data:
                    z_data = fill_buffer(datasize_Main, serObj)
                else:
                    continue
                visualize_data_time_only(x_data, y_data, z_data, sampling_frequency, fig, axs)

        # plot functions
        # check for model file existence
        # show_message("Information", "Just Visualize")

    def Visualize_Data_With_ML_Model():
        serObj = ComOK()[0]
        if serObj is None:
            show_message("Error", "Cannot collect data!\nPlug the Device!\nStart Communication First!")
        else:
            fig, axs = plt.subplots(1, 3, figsize=(5, 5))

            anomaly_indices = []
            x_data = [0.0] * datasize_Main
            y_data = [0.0] * datasize_Main
            z_data = [0.0] * datasize_Main

            while True:
                received_data = str(serObj.readline())[2:-5].casefold()
                print(received_data)

                if received_data == "x":
                    x_data = fill_buffer(datasize_Main, serObj)
                    continue
                elif received_data == "y":
                    y_data = fill_buffer(datasize_Main, serObj)
                    continue
                elif received_data == "z":
                    z_data = fill_buffer(datasize_Main, serObj)

                    print("Getting predictions...")

                    anomaly_indices.clear()
                    anomaly_indices.append(predict(trained_models[0][0], trained_models[0][1], trained_models[0][2],
                                                   np.array(x_data).reshape(-1, 1)))
                    anomaly_indices.append(predict(trained_models[1][0], trained_models[1][1], trained_models[1][2],
                                                   np.array(y_data).reshape(-1, 1)))
                    anomaly_indices.append(predict(trained_models[2][0], trained_models[2][1], trained_models[2][2],
                                                   np.array(z_data).reshape(-1, 1)))
                else:
                    continue

                visualize_data_time_only(x_data, y_data, z_data, sampling_frequency, fig, axs)

                print(x_data)
                print(y_data)
                print(z_data)

                print("Anomaly indices...")
                print(anomaly_indices[0])
                print(anomaly_indices[1])
                print(anomaly_indices[2])

                visualize_anomalies(x_data, y_data, z_data, anomaly_indices[0], anomaly_indices[1], anomaly_indices[2],
                                    sampling_frequency, fig, axs)

        # plot functions
        # check for model file existence
        show_message("Information", "Visualize anomalies")

    visualizeWithAnomaliesBtn = tk.Button(main_frame)
    visualizeWithAnomaliesBtn["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    visualizeWithAnomaliesBtn["font"] = ft
    visualizeWithAnomaliesBtn["fg"] = "#000000"
    visualizeWithAnomaliesBtn["justify"] = "center"
    visualizeWithAnomaliesBtn["text"] = "Data Visualization With Anomalies"
    visualizeWithAnomaliesBtn.place(x=20, y=50, width=200, height=40)
    visualizeWithAnomaliesBtn["command"] = Visualize_Data_With_ML_Model

    justDataVisualizeBtn = tk.Button(main_frame)
    justDataVisualizeBtn["bg"] = "#f0f0f0"
    ft = tkFont.Font(family='Times', size=10)
    justDataVisualizeBtn["font"] = ft
    justDataVisualizeBtn["fg"] = "#000000"
    justDataVisualizeBtn["justify"] = "center"
    justDataVisualizeBtn["text"] = "Data Visualization"
    justDataVisualizeBtn.place(x=20, y=120, width=200, height=40)
    justDataVisualizeBtn["command"] = Just_Visualize_Data

    Visualize_Data_Frame.pack(pady=20)


def About_US_Page():
    About_US_Frame = tk.Frame(main_frame)

    # URL
    website = "http://vibroguard.unaux.com/"

    # Label to display the URL as a hyperlink
    url_label = tk.Label(About_US_Frame, text="Visit our website", fg="blue", cursor="hand2")
    url_label.pack()

    # Function to open the URL when the label is clicked
    def open_website(event):
        import webbrowser
        webbrowser.open_new(website)

    # Bind the label to the function so that it opens the URL when clicked
    url_label.bind("<Button-1>", open_website)
    About_US_Frame.pack(pady=20)


def hide_all_indicators():
    Select_COM_Port_Btn_Indicator.config(bg='#c3c3c3')
    Collect_Data_Btn_Indicator.config(bg='#c3c3c3')
    Train_ML_Model_Btn_Indicator.config(bg='#c3c3c3')
    Visualize_Data_Btn_Indicator.config(bg='#c3c3c3')
    About_US_Btn_Indicator.config(bg='#c3c3c3')


def delete_pages():
    for frame in main_frame.winfo_children():
        frame.destroy()


def indicate(lb, page):
    hide_all_indicators()
    lb.config(bg="blue")
    delete_pages()
    page()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x400")
    root.title("VIBROGUARD")
    root.resizable(False, False)

    options_frame = tk.Frame(root, bg='#c3c3c3')
    options_frame.pack(side=tk.LEFT)
    options_frame.pack_propagate(False)
    options_frame.configure(width=130, height=400)

    # Buttons for pages
    # Select COM Port
    # Collect Data
    # Train ML Model
    # Visualize Data
    Select_COM_Port_Btn = tk.Button(options_frame, text="Select COM Port", bg='#c3c3c3',
                                    command=lambda: indicate(Select_COM_Port_Btn_Indicator, Select_COM_Port_Page))
    Select_COM_Port_Btn.place(x=10, y=50, width=110, height=40)
    Select_COM_Port_Btn_Indicator = tk.Label(options_frame, text="", bg='#c3c3c3')
    Select_COM_Port_Btn_Indicator.place(x=3, y=50, width=5, height=40)

    Collect_Data_Btn = tk.Button(options_frame, text="Collect Data", bg='#c3c3c5',
                                 command=lambda: indicate(Collect_Data_Btn_Indicator, Collect_Data_Page))
    Collect_Data_Btn.place(x=10, y=120, width=110, height=40)
    Collect_Data_Btn_Indicator = tk.Label(options_frame, text="", bg='#c3c3c3')
    Collect_Data_Btn_Indicator.place(x=3, y=120, width=5, height=40)

    Train_ML_Model_Btn = tk.Button(options_frame, text="Train ML Model", bg='#c3c3c3',
                                   command=lambda: indicate(Train_ML_Model_Btn_Indicator, Train_ML_Model_Page))
    Train_ML_Model_Btn.place(x=10, y=190, width=110, height=40)
    Train_ML_Model_Btn_Indicator = tk.Label(options_frame, text="", bg='#c3c3c3')
    Train_ML_Model_Btn_Indicator.place(x=3, y=190, width=5, height=40)

    Visualize_Data_Btn = tk.Button(options_frame, text="Visualize Data", bg='#c3c3c3',
                                   command=lambda: indicate(Visualize_Data_Btn_Indicator, Visualize_Data_Page))
    Visualize_Data_Btn.place(x=10, y=260, width=110, height=40)
    Visualize_Data_Btn_Indicator = tk.Label(options_frame, text="", bg='#c3c3c3')
    Visualize_Data_Btn_Indicator.place(x=3, y=260, width=5, height=40)

    About_US_Btn = tk.Button(options_frame, text="About Us", bg='#c3c3c3',
                             command=lambda: indicate(About_US_Btn_Indicator, About_US_Page))
    About_US_Btn.place(x=10, y=330, width=110, height=40)
    About_US_Btn_Indicator = tk.Label(options_frame, text="", bg='#c3c3c3')
    About_US_Btn_Indicator.place(x=3, y=330, width=5, height=40)

    main_frame = tk.Frame(root, highlightbackground='black', highlightthickness=1)
    main_frame.pack(side=tk.LEFT)
    main_frame.pack_propagate(False)
    main_frame.configure(width=400, height=500)

    showTimeLabel = tk.Label(root)
    showTimeLabel["bg"] = "#ffffff"
    ft = tkFont.Font(family='Times', size=10)
    showTimeLabel["font"] = ft
    showTimeLabel["fg"] = "#333333"
    showTimeLabel["justify"] = "center"
    showTimeLabel["text"] = ""
    showTimeLabel.place(x=380, y=360, width=110, height=30)

    update_time()

    root.mainloop()
