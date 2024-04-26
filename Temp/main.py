import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main Screen")
        self.geometry("800x600")
        self.attributes("-fullscreen", True)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.figure = plt.figure(figsize=(6, 4))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.plot_button = ttk.Button(self.main_frame, text="Show Graph", command=self.update_graph)
        self.plot_button.pack(pady=20)

        self.train_button = ttk.Button(self.main_frame, text="Train")
        self.train_button.pack(pady=10)

        self.collect_button = ttk.Button(self.main_frame, text="Collect")
        self.collect_button.pack(pady=10)

        self.switch_to_second_page_button = ttk.Button(self.main_frame, text="Go to Second Page", command=self.switch_to_second_page)
        self.switch_to_second_page_button.pack(pady=20)

        self.minimize_button = ttk.Button(self.main_frame, text="Minimize", command=self.minimize_window)
        self.minimize_button.pack(side=tk.RIGHT, padx=5)

        self.change_size_button = ttk.Button(self.main_frame, text="Change Size", command=self.toggle_fullscreen)
        self.change_size_button.pack(side=tk.RIGHT, padx=5)

        self.close_button = ttk.Button(self.main_frame, text="Close", command=self.close_program)
        self.close_button.pack(side=tk.RIGHT, padx=5)

    def update_graph(self):
        x = range(10)
        y = [random.randint(0, 10) for _ in range(10)]
        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.set_title('Sample Graph')
        self.ax.grid(True)
        self.canvas.draw()

    def switch_to_second_page(self):
        self.second_page = SecondPage(self)
        self.second_page.show()

    def minimize_window(self):
        self.iconify()

    def toggle_fullscreen(self):
        if self.attributes("-fullscreen"):
            self.attributes("-fullscreen", False)
        else:
            self.attributes("-fullscreen", True)

    def close_program(self):
        self.destroy()

class SecondPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Second Screen")
        self.geometry("800x600")
        self.attributes("-fullscreen", True)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.back_button = ttk.Button(self.main_frame, text="Go to Main Page", command=self.switch_to_main_page)
        self.back_button.pack(pady=20)

        self.text = """
        This is some sample text.
        You can customize it as needed.
        """
        self.text_label = tk.Label(self.main_frame, text=self.text, wraplength=600, justify=tk.LEFT)
        self.text_label.pack(pady=20)

        self.figure = plt.figure(figsize=(6, 4))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.close_button = ttk.Button(self, text="Close", command=self.close_program)
        self.close_button.pack(side=tk.RIGHT, padx=5)

    def switch_to_main_page(self):
        self.destroy()

    def close_program(self):
        self.master.close_program()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
