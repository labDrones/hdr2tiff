from tkinter import filedialog
import tkinter as tk
from . import raster

class Controller():
    def __init__(self) -> None:
        pass
    def say_hi(self):
        dir =  filedialog.askdirectory()
        raster.get_tiffs(dir)
        print("hi there, everyone!", "hu")
    
    def teste(self, place):
        place.addons.append(tk.Button())
        place.addons[-1]["text"] = "ddss\n(click me)"
        place.addons[-1]["command"] = lambda: place.controller.teste(place)
        place.addons[-1].pack(side="bottom")