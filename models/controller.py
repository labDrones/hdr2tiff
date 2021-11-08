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
        expression = "648-650, 550-552, 450-452"
        # print("Waveee", waves)
        selc  = voo.get_bands_by_intervals(waves, expression)
        for r in rasterizes:
            print(r)
            print(voo.make_tiff_of(name=r, bands=selc))
        print("Waveaaaaee",  len(selc))        # print("tesaet", voo.get_rasterizes())
    
    def teste(self, place):
        place.addons.append(tk.Button())
        place.addons[-1]["text"] = "ddss\n(click me)"
        place.addons[-1]["command"] = lambda: place.controller.teste(place)
        place.addons[-1].pack(side="bottom")



