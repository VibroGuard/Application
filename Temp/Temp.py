import tkinter as tk

class SampleApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("800x600")
        self.title("Page Navigation")

        # Container to hold all pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Dictionary to hold frames of all pages
        self.frames = {}

        # Define all pages
        for PageClass in (Page1, Page2, Page3, Page4):
            page_name = PageClass.__name__
            frame = PageClass(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the first page by default
        self.show_frame("Page1")

        # Navigation bar
        nav_frame = tk.Frame(self)
        nav_frame.pack(anchor="nw", padx=10, pady=10)

        for page_name in self.frames:
            button = tk.Button(nav_frame, text=page_name, command=lambda name=page_name: self.show_frame(name))
            button.pack(side="left", padx=5)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Page 1")
        label.pack(side="top", fill="x", pady=10)

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Page 2")
        label.pack(side="top", fill="x", pady=10)

class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Page 3")
        label.pack(side="top", fill="x", pady=10)

class Page4(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Page 4")
        label.pack(side="top", fill="x", pady=10)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
