import tkinter as tk
from tkinter import filedialog
from models.controller import Controller

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = Controller()
        self.master = master
        self.master.geometry("960x640+300+300")
        self.master.title("HDR to TIFF")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.controller.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                            command=self.master.destroy)
        self.quit.pack(side="bottom")

    # def say_hi(self):
    #     base_dir = filedialog.askdirectory()
    #     self.hi_there["text"] = "Hello everyone\n(click me)"
    #     print("hi there, everyone!", base_dir)

root = tk.Tk()
app = Application(master=root)
app.mainloop()