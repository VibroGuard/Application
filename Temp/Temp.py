import tkinter as tk
from tkinter import messagebox, ttk


def show_progress_bar():
    # Create a custom message box
    progress_box = tk.Toplevel()
    progress_box.title("Progress")

    # Add a label
    label = tk.Label(progress_box, text="Loading...")
    label.pack(pady=10)

    # Add a progress bar
    progress_bar = ttk.Progressbar(progress_box, length=200, mode='indeterminate')
    progress_bar.pack(pady=10)

    # Start the progress bar
    progress_bar.start(10)  # Adjust the speed of the progress bar

    # Close the progress box after some time (e.g., 5 seconds)
    progress_box.after(5000, progress_box.destroy)


# Create a Tkinter window
root = tk.Tk()
root.geometry("300x200")

# Button to show the progress bar
btn = tk.Button(root, text="Show Progress", command=show_progress_bar)
btn.pack(pady=20)

root.mainloop()
