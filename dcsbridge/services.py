import sys
import os
from pathlib import Path
from dcsbridge.dataloaders.file import TextFileDataLoader

__THEATERS = {
    "caucasus" : "Caucasus",
    "mariana" : "Mariana",
    "nevada" : "Nevada",
    "pg" : "Persian Gulf",
    "syria" : "Syria"
}


def load_aerodromes(theater):
    directory = None
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        directory = Path(sys._MEIPASS)
    else:
        directory = Path(os.getcwd()) / Path("resources") / Path("aerodromes")
    dl = TextFileDataLoader(directory / Path(f"{__THEATERS[theater]}.csv"))
    dl.load_data()
    return dl.get_waypoints()
