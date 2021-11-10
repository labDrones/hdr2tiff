from tkinter import DoubleVar, filedialog
import tkinter as tk
from . import raster
from .hdr import Fly

class Controller():
    def __init__(self, dir:str = '', alt:float = 100, lens:float = 12 ) -> None:
        self.__dir:str = dir 
        self.__alt:float = alt
        self.__lens:float = lens

    def set_dir(self, dir:str)->None:
        self.__dir = dir

    def get_dir(self)->str:
        return self.__dir
    
    def set_alt(self, alt: float)->None:
        self.__alt = alt
    
    def get_alt(self)->float:
        return self.__alt

    def set_lens(self, lens: float)->None:
        self.__lens = lens
    
    def get_lens(self)->float:
        return self.__lens

    def get_waves_by_expression(self, expression):
        voo = Fly(self.__dir, self.__alt, self.__lens)
        rasterizes = voo.get_rasterizes()
        waves = voo.get_waves(rasterizes[0])
        filtred_waves  = voo.get_bands_by_intervals(waves, expression)
        return filtred_waves
    
    def get_rasterizebles(self):
        voo = Fly(self.__dir, self.__alt, self.__lens)
        return voo.get_rasterizes()

    def maketiffs(self, expression, targets):
        voo = Fly(self.__dir, self.__alt, self.__lens)
        selc  = self.get_waves_by_expression(expression)
        log = dict()
        log["files"] = list()
        for r in targets:
            name = r
            result = voo.make_tiff_of(name=r, bands=selc)
            print(name, result)
            log["files"].append((name, result))

        log["bands"] = selc
        return log

    def teste(self, place):
        place.addons.append(tk.Button())
        place.addons[-1]["text"] = "ddss\n(click me)"
        place.addons[-1]["command"] = lambda: place.controller.teste(place)
        place.addons[-1].pack(side="bottom")



