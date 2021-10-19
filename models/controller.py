from tkinter import filedialog
import tkinter as tk
from . import raster
from .hdr import Fly

class Controller():
    def __init__(self) -> None:
        pass
    def say_hi(self):
        dir =  filedialog.askdirectory()
        voo = Fly(dir, 100, 12)
        # if voo.__check_imu():

        #     imu =  filedialog.askopenfilename()
        #     voo.set_imu(imu)
        print()
        # print("tesaet", voo.get_rasterizes())
    
    def teste(self, place):
        place.addons.append(tk.Button())
        place.addons[-1]["text"] = "ddss\n(click me)"
        place.addons[-1]["command"] = lambda: place.controller.teste(place)
        place.addons[-1].pack(side="bottom")