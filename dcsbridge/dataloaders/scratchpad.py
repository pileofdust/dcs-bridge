import re
from pathlib import Path
import logging


class ScratchpadDataLoader:
    # N 37°47.332', W 114°25.693'
    # 1497m, 4913ft
    __coordinates_pattern = re.compile(r"([NS]) (\d+)[°˚](\d+).(\d+)\', ([WE]) (\d+)[°˚](\d+).(\d+)\'")
    __altitude_pattern = re.compile(r"(\d+)m, (\d+)ft")
    __bingo_pattern = re.compile(r"\A(\d+)")
    __command_pattern = re.compile(r"\A#(\d+) - ([\w ]+)|\A#(\d+)|\A#(\w+) - ([\w ]+)|\A#(\w+)")

    __SCRATCHPAD_FILE = Path.home() / \
        Path("Saved Games") / Path("DCS.openbeta") / Path("Scratchpad") / Path("0000.txt")

    def __init__(self, data_file=__SCRATCHPAD_FILE):
        if not data_file:
            data_file = self.__SCRATCHPAD_FILE
        self.__data_file_path = Path(data_file)
        self.__waypoints = {}

    def __reset_data(self):
        self.__waypoints = {}

    def load_data(self):
        self.__reset_data()

        logging.info(f"Loading data from: {self.__data_file_path}")
        lines = None
        with open(self.__data_file_path, encoding="UTF-8") as file:
            lines = file.readlines()

        idx = 1
        lines_iterator = iter(lines)

        lat, lon, alt = None, None, None
        for line in lines_iterator:
            cmd = self.__command_pattern.match(line)
            if cmd is not None:
                index_with_arg, index_with_arg_value,\
                    index_without_arg, cmd_with_arg,\
                    cmd_with_arg_value, cmd_without_arg = cmd.groups()

                if index_without_arg:
                    idx = int(index_without_arg)
                elif index_with_arg:
                    idx = int(index_with_arg)
                elif cmd_without_arg:
                    self.__handle_command(lines_iterator, cmd_without_arg)
                elif cmd_with_arg:
                    self.__handle_command(lines_iterator, cmd_with_arg, cmd_with_arg_value)
            else:
                coordinates = None if lat is not None else self.__coordinates_pattern.match(line)
                altitude = None if alt is not None else self.__altitude_pattern.match(line)

                if coordinates is not None:
                    t = coordinates.groups()
                    lat = f"{t[0]}{t[1]}{t[2]}{t[3]}"
                    lon = f"{t[4]}{int(t[5]):03d}{t[6]}{t[7]}"
                elif altitude is not None:
                    alt = altitude.groups()[-1]

                if lat is not None and lon is not None and alt is not None:
                    self.__waypoints[idx] = (lat, lon, alt)
                    idx = idx + 1
                    lat, lon, alt = None, None, None

    def __handle_command(self, lines_iterator, cmd:str, cmd_args:str=None):
        if cmd.lower() == "bingo":
            for l in lines_iterator:
                value = self.__bingo_pattern.match(l)
                if value:
                    self.__bingo = value.groups()[0]
                    break


    def get_waypoints(self):
        return self.__waypoints

    def get_waypoint(self, index):
        return self.__waypoints[index]

    def get_bingo(self):
        return self.__bingo
