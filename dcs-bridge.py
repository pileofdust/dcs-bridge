from dcsbridge.drivers.f16 import Driver
from dcsbridge.dataloaders.combatflite import MissionPlanDataLoader
from dcsbridge.dataloaders.common import DataLoader
from dcsbridge.dataloaders.scratchpad import ScratchpadDataLoader
from time import localtime
from pathlib import Path
import sys
import socket

__default_bingo = "4000"


class DcsBios:
    def __init__(self, host="localhost", port=7778):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__host = host
        self.__port = port

    def send(self, msg):
        self.__connection.sendto(msg.encode("utf-8"), (self.__host, self.__port))


def main(argv):
    num_args = len(argv)
    if num_args < 2:
        raise Exception("No commandline argument")

    dcsbios = DcsBios()
    d = Driver(dcsbios)

    if "mission" == argv[1]:  # Load mission plan from CombatFlite: mission
        dl = MissionPlanDataLoader()
        dl.load_data()
        d.enter_steerpoints(dl.get_waypoints())
        d.enter_bingo(dl.get_bingo())
    elif "bingo" == argv[1]:  # Set bingo value: bingo <value>
        if num_args == 3:
            d.enter_bingo(argv[2])
        else:
            d.enter_bingo(__default_bingo)
    elif "time" == argv[1]:  # Set aircraft system time to local time: time
        d.enter_time(localtime())
    elif "index" == argv[1]:  # Load objective index: index <data file> <index>
        if num_args < 4:
            raise Exception("Invalid arguments: index <data file> <index>")

        data_file = argv[2]
        index = argv[3]

        dl = DataLoader(data_file)
        dl.load_data()
        d.enter_steerpoint(dl.get_waypoint(index))
    elif "scratchpad" == argv[1]: # Load steerpoints from DCS Scratchpad files
        data_file = Path("Scratchpad") / Path("0000.txt")
        if num_args == 3:
            data_file = Path(argv[2])

        dl = ScratchpadDataLoader(data_file)
        dl.load_data()
        d.enter_steerpoints(dl.get_waypoints())
    else:
        raise Exception("Unsupported operation")


if __name__ == "__main__":
    try:
        main(sys.argv)
    except Exception:
        raise
