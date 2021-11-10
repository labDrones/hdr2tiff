# from _typeshed import Self
import tkinter as tk
from tkinter import ttk
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
        separator = ttk.Separator(self.master, orient='horizontal')
        separator.pack(fill='x')
        self.create_lens_container()
        separator = ttk.Separator(self.master, orient='horizontal')
        separator.pack(fill='x')
        self.create_expression_container()
        separator = ttk.Separator(self.master, orient='horizontal')
        separator.pack(fill='x')
        self.create_path_container()
        separator = ttk.Separator(self.master, orient='horizontal')
        separator.pack(fill='x')
        self.create_start_container()
        separator = ttk.Separator(self.master, orient='horizontal')
        separator.pack(fill='x')
        self.create_log_container()
        separator = ttk.Separator(self.master, orient='horizontal')
        separator.pack(fill='x')
    
    def create_log_container(self)->None:
        self.log_container = tk.Frame(self.master)



    def create_start_container(self)->None:
        self.start_container = tk.Frame(self.master)
        self.start_container.pack()
        self.start_button = tk.Button(self.start_container)
        self.start_button["bg"] = "#00FF00"
        self.start_button["text"] = "Iniciar processo\n(click me)"
        self.start_button["command"] = lambda: self.start()
        self.start_button.pack(side=tk.TOP)

    def start(self)->None:
        alt = float(self.alt.get().replace(",", ".")) 
        lens = float(self.variable_lens.get())
        self.controller.set_alt(alt)
        self.controller.set_lens(lens)

        expression = self.expression.get()
        expression = expression if len(expression) > 1 else ">0"

        logs = self.controller.maketiffs(expression, self.get_targets())
        

    def get_targets(self):
        return  self.controller.get_rasterizebles()

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
        self.lens_label = tk.Label(self.lens_container)
        self.lens_label["font"] = self.fontePadrao
        self.lens_label["text"] = "Lentes usada: "
        self.lens_label.pack(side=tk.LEFT) 
        self.variable_lens = tk.StringVar(self.lens_container)
        self.variable_lens.set(focal_Options[2]) # default value

        w = tk.OptionMenu(self.lens_container, self.variable_lens, *focal_Options)
        w.pack(side=tk.RIGHT)


    def set_path(self):
        dir =  filedialog.askdirectory()
        self.controller.set_dir(dir)
        self.path_label["text"] = dir

    def create_path_container(self)->None:
        self.path_container = tk.Frame(self.master)
        self.path_container.pack()
        self.get_path_button = tk.Button(self.path_container)
        self.get_path_button["text"] = "Selecionar pasta do voo\n(click me)"
        self.get_path_button["command"] = lambda: self.set_path()
        self.get_path_button.pack(side=tk.LEFT)
        self.path_label = tk.Label(self.path_container)
        self.path_label["font"] = self.fontePadrao
        self.path_label["text"] = ""
        self.path_label.pack(side=tk.RIGHT  ) 

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
        self.create_containers()





if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
    #250-350,450-460,560-750