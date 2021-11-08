import tkinter as tk
from tkinter import filedialog
from models.controller import Controller

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = Controller()
        self.fontePadrao = ("Arial", "10")
        self.master = master
        self.addons = []
        self.master.geometry("960x640+300+300")
        self.master.title("HDR to TIFF")
        self.pack()
        self.create_widgets()

    def create_containers(self)->None:
        self.create_alt_container()
        self.create_lens_container()
        self.create_path_container()
    
    def create_alt_container(self)->None:
        self.alt_container = tk.Frame(self.master)
        self.alt_container.pack()
        self.alt_label = tk.Label(self.alt_container)
        self.alt_label["font"] = self.fontePadrao
        self.alt_label["text"] = "Altura do voo em metros: "
        self.alt_label.pack(side=tk.LEFT)    
        self.alt = tk.Entry(self.alt_container)
        self.alt["width"] = 30
        self.alt["font"] = self.fontePadrao
        self.alt.pack(side=tk.RIGHT)
    
    def create_lens_container(self)->None:
        self.lens_container = tk.Frame(self.master)
        self.lens_container.pack()
        focal_Options = [ '4.8', 
                '8.0',
                '12.0',
                '17.0',
                '23.0',
                '35.0']
        variable = tk.StringVar(self.lens_container)
        variable.set(focal_Options[2]) # default value

        w = tk.OptionMenu(self.lens_container, variable, *focal_Options)
        w.pack(side=tk.RIGHT)


    
    def create_path_container(self)->None:
        self.path_container = tk.Frame(self.master)
        self.path_container.pack()
        self.hi_there = tk.Button(self.path_container)
        self.hi_there["text"] = "Selecionar pasta do voo\n(click me)"
        self.hi_there["command"] = lambda: self.controller.say_hi()
        self.hi_there.pack(side="top")

    def create_expression_container(self):
        self.expression_container = tk.Frame(self.master)
        self.expression_container.pack()
        self.expression_label = tk.Label(self.expression_container)
        self.expression_label["font"] = self.fontePadrao
        self.expression_label["text"] = "Expressão das bandas: "
        self.expression_label.pack(side=tk.LEFT)    
        self.expression = tk.Entry(self.expression_container)
        self.expression["width"] = 30
        self.expression["font"] = self.fontePadrao
        self.expression.pack(side=tk.RIGHT)

    def create_widgets(self)->None:
        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                     command=self.master.destroy)
        # self.quit.pack(side="bottom")
        self.create_containers()
        self.create_lens_entry()
        self.create_path_entry()




if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()