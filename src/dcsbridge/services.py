from importlib.resources import files

from dcsbridge.dataloaders.file import TextFileDataLoader


__THEATERS = {"caucasus": "Caucasus", "mariana": "Mariana", "nevada": "Nevada", "pg": "Persian Gulf", "syria": "Syria"}


def load_aerodromes(theater):
    datafile = files("dcsbridge.resources.aerodromes").joinpath(f"{__THEATERS[theater]}.csv")
    dl = TextFileDataLoader(datafile)
    dl.load_data()

    return dl.get_waypoints()
