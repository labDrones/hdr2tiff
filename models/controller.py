from tkinter import filedialog
from . import raster

class Controller():
    def __init__(self) -> None:
        pass
    def say_hi(self):
        dir =  filedialog.askdirectory()
        raster.get_tiffs(dir)
        print("hi there, everyone!", "hu")
