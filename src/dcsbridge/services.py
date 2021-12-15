from pathlib import Path
from dcsbridge.dataloaders.file import TextFileDataLoader
from importlib.resources import files

__THEATERS = {"caucasus": "Caucasus", "mariana": "Mariana", "nevada": "Nevada", "pg": "Persian Gulf", "syria": "Syria"}


def load_aerodromes(theater):
    datafile = files("dcsbridge.resources.aerodromes").joinpath(f"{__THEATERS[theater]}.csv")
    dl = TextFileDataLoader(datafile)
    dl.load_data()

    return dl.get_waypoints()
