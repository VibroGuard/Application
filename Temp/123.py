import tkinter as tk
from tkinter import ttk
import threading
import time


def train():
    """Function to simulate training process."""
    progress_window = tk.Toplevel(root)
    progress_window.title("Training Progress")
    progress_window.geometry("300x100")

    progress_label = tk.Label(progress_window, text="Training in progress...")
    progress_label.pack(pady=10)

    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", mode="indeterminate")
    progress_bar.pack(expand=True, fill=tk.X, padx=20)
    progress_bar.start()

    root.withdraw()  # Hide the main window

    # Simulate training process for 10 seconds
    time.sleep(10)

    progress_bar.stop()
    progress_window.destroy()
    root.deiconify()  # Show the main window


def train_button_clicked():
    """Function to handle train button click."""
    root.config(cursor="wait")  # Change cursor to wait
    threading.Thread(target=train).start()  # Start training process in a separate thread
    # No need to unfreeze the main window explicitly, it's handled in the train() function


# Main Tkinter application
root = tk.Tk()
root.title("Training App")

# Create train button
train_button = tk.Button(root, text="Train", command=train_button_clicked)
train_button.pack(pady=20)

root.mainloop()
