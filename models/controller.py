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
        rasterizes = voo.get_rasterizes()
        waves = voo.get_waves(rasterizes[0])
        expression = "<500,450-780,>890, 991.5"
        print("Waveee", waves)
        # print("tesaet", voo.get_rasterizes())
    
    def teste(self, place):
        place.addons.append(tk.Button())
        place.addons[-1]["text"] = "ddss\n(click me)"
        place.addons[-1]["command"] = lambda: place.controller.teste(place)
        place.addons[-1].pack(side="bottom")