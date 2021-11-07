import openpyxl
import re
from pathlib import Path


class DataLoader:
    def __init__(self):
        self.__waypoints = {}

    def _reset_data(self):
        self.__waypoints = {}

    def _add_waypoint(self, idx, lat, lon, alt):
        self.__waypoints[str(idx)] = (lat, lon, str(alt))

    def get_waypoints(self):
        return self.__waypoints

    def get_waypoint(self, index):
        return self.__waypoints[index]


class ExcelDataLoader(DataLoader):
    __INDEX_COLUMN = 0
    __COORDINATE_COLUMN = 1
    __ALTITUDE_COLUMN = 2

    ###
    # waypoint = (idx, lat / lon, alt)
    ###

    # 35°44.0705'N 37°06.23947'E
    __coordinates_pattern = re.compile(r"(\d+)[°˚](\d+).(\d+)\'([NS]) (\d+)[°˚](\d+).(\d+)\'([EW])")

    def __init__(self, data_file):
        super().__init__()
        data_file_path = Path(data_file)
        wb = openpyxl.load_workbook(data_file_path)
        self.__ws = wb.worksheets[0]

    def __parse_row(self, row):
        idx = row[self.__INDEX_COLUMN]
        coordinates = row[self.__COORDINATE_COLUMN]
        altitude = row[self.__ALTITUDE_COLUMN]

        if not altitude:
            altitude = "0"
        else:
            altitude = round(altitude)

        t = self.__coordinates_pattern.match(coordinates).groups()
        lat = f"{t[3]}{t[0]}{t[1]}{t[2]}"
        lon = f"{t[7]}{int(t[4]):03d}{t[5]}{t[6]}"

        self._add_waypoint(idx, lat, lon, altitude)

    def load_data(self):
        self._reset_data()

        for row in self.__ws.iter_rows(2, self.__ws.max_row, 1, self.__ws.max_column, True):
            for cell in row:
                self.__parse_row(row)
                break
