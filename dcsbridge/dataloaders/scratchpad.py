import re
from pathlib import Path


class ScratchpadDataLoader:
    __waypoints = {}

    # N 37°47.332', W 114°25.693'
    # 1497m, 4913ft
    __coordinates_pattern = re.compile(r"([NS]) (\d+)[°˚](\d+).(\d+)\', ([WE]) (\d+)[°˚](\d+).(\d+)\'")
    __altitude_pattern = re.compile(r"(\d+)m, (\d+)ft")
    __command_pattern = re.compile(r"\A#(\d+) - ([\w ]+)|\A#(\d+)|\A#(\w+) - ([\w ]+)|\A#(\w+)")

    __CMD_STEERPOINT_NUM = 2
    __CMD_STEERPOINT_NUM_WITH_ARG = 0
    __CMD_NAME = 3
    __CMD_NAME_WITH_ARG = 5

    def __init__(self, data_file):
        self.__data_file_path = data_file_path = Path(data_file)

    def __reset_data(self):
        self.__waypoints = {}

    def load_data(self):
        self.__reset_data()

        lines = None
        with open(self.__data_file_path, encoding="UTF-8") as file:
            lines = file.readlines()

        idx = 1
        lines_iterator = iter(lines)
        for line in lines_iterator:
            cmd = self.__command_pattern.match(line)
            if cmd:
                cmd_groups = cmd.groups()
                if cmd_groups[self.__CMD_STEERPOINT_NUM]:
                    idx = int(cmd_groups[self.__CMD_STEERPOINT_NUM])
                elif cmd_groups[self.__CMD_STEERPOINT_NUM_WITH_ARG]:
                    idx = int(cmd_groups[self.__CMD_STEERPOINT_NUM_WITH_ARG])
                continue
            coordinates = self.__coordinates_pattern.match(line)
            if coordinates:
                t = coordinates.groups()
                lat = f"{t[0]}{t[1]}{t[2]}{t[3]}"
                lon = f"{t[4]}{int(t[5]):03d}{t[6]}{t[7]}"
                alt_line = next(lines_iterator)
                alt = self.__altitude_pattern.match(alt_line).groups()[-1]
                self.__waypoints[idx] = (lat, lon, alt)
                idx = idx + 1

    def get_waypoints(self):
        return self.__waypoints

    def get_waypoint(self, index):
        return self.__waypoints[index]
