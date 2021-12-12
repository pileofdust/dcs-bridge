import logging
import re


class DataLoader:
    _INDEX_COLUMN = 0
    _COORDINATE_COLUMN = 1
    _ALTITUDE_COLUMN = 2

    # 35°44.0705'N 37°06.23947'E
    _coordinates_pattern = re.compile(r"(\d+)[°˚](\d+).(\d+)\'([NS]) (\d+)[°˚](\d+).(\d+)\'([EW])")

    def __init__(self):
        self.__waypoints = {}

    def _reset_data(self):
        self.__waypoints = {}

    def _add_waypoint(self, idx, lat, lon, alt):
        self.__waypoints[str(idx)] = (lat, lon, str(alt))

    def _add_row_as_waypoint(self, row):
        logging.debug(row)
        idx = row[self._INDEX_COLUMN]
        lat, lon = self._parse_coordinates(row[self._COORDINATE_COLUMN])
        altitude = self._parse_altitude(row[self._ALTITUDE_COLUMN])

        self._add_waypoint(idx, lat, lon, altitude)

    def _parse_coordinates(self, coordinates):
        logging.debug(coordinates)
        t = self._coordinates_pattern.match(coordinates).groups()
        lat = f"{t[3]}{t[0]}{t[1]}{t[2]}"
        lon = f"{t[7]}{int(t[4]):03d}{t[5]}{t[6]}"

        return lat, lon

    def _parse_altitude(self, altitude):
        if not altitude:
            altitude = "0"
        elif type(altitude) is not str:
            altitude = str(round(altitude))

        return altitude

    def get_waypoints(self):
        return self.__waypoints

    def get_waypoint(self, index):
        return self.__waypoints[index]
