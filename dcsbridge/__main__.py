from dcsbridge.drivers.f16 import Driver
from dcsbridge.dataloaders.combatflite import MissionPlanDataLoader
from dcsbridge.dataloaders.file import TextFileDataLoader
from dcsbridge.dataloaders.scratchpad import ScratchpadDataLoader
from time import localtime
from pathlib import Path
import sys
import os
import socket
import argparse
import logging

__DEFAULT_BINGO = "4000"
__PROGRAM_NAME = "dcs-bridge"


class DcsBios:
    def __init__(self, host="localhost", port=7778):
        self.__connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__host = host
        self.__port = port

    def send(self, msg):
        self.__connection.sendto(msg.encode("utf-8"), (self.__host, self.__port))


def execute_mission(driver, args):
    dl = MissionPlanDataLoader()
    dl.load_data()
    driver.enter_steerpoints(dl.get_waypoints())
    driver.enter_bingo(dl.get_bingo())


def execute_bingo(driver, args):
    driver.enter_bingo(args.bingo)


def execute_time(driver, args):
    if "local" == args.timezone:
        driver.enter_time(localtime())


def execute_index(driver, args):
    dl = TextFileDataLoader(args.file, columns=args.columns)
    dl.load_data()
    driver.enter_steerpoint(dl.get_waypoint(str(args.index)))


def execute_aerodrome(driver, args):
    driver.enter_steerpoint(load_aerodromes(args.theater)[str(args.id)])


def execute_scratchpad(driver, args):
    dl = ScratchpadDataLoader(args.file)
    dl.load_data()
    driver.enter_steerpoints(dl.get_waypoints())


def parse_arguments(argv):
    parser = argparse.ArgumentParser(prog=__PROGRAM_NAME)
    parser.add_argument("-v", "--verbose", required=False, action="store_true", help="enable output verbosity")
    parser.add_argument("-vv", "--debug", required=False, action="store_true", help="enable debug output")

    subparser = parser.add_subparsers(dest="command")
    mission = subparser.add_parser("mission")
    bingo = subparser.add_parser("bingo")
    time = subparser.add_parser("time")
    index = subparser.add_parser("index")
    aerodrome = subparser.add_parser("aerodrome")
    scratchpad = subparser.add_parser("scratchpad")

    mission.add_argument("file", type=str, help="path to excel file with mission plan")
    mission.add_argument("--default-bingo", type=int, required=False, default=__DEFAULT_BINGO,
                         help="default bingo value if mission from mission plan")

    bingo.add_argument("bingo", type=int, help="bingo value to set in airframe")

    time.add_argument("timezone", type=str, default='local', choices=['local'],
                      help="timezone to use when entering current time")

    index.add_argument("file", type=str, help="path to data file")
    index.add_argument("index", type=int, help="index value of entry to load")
    index.add_argument("--columns", "--cols", type=str, required=False,
                       help="list of data column number in the format id,coordinates,altitude")

    aerodrome.add_argument("theater", choices=["caucasus", "nevada", "syria", "pg", "mariana"])
    aerodrome.add_argument("id", type=int, help="id of aerodrome to load")

    scratchpad.add_argument("file", type=str, nargs="?",
        help="file where DCS Scratchpad coordinates are stored, defaults to 0000.txt in default Scratchpad folder")

    return parser.parse_args(argv)


def enable_logging(argv):
    if argv.verbose:
        logging.basicConfig(level=logging.INFO)
    elif argv.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)


def main(argv):
    args = parse_arguments(argv)

    enable_logging(args)

    if args.command:
        dcsbios = DcsBios()
        d = Driver(dcsbios)

        handlers = {
            "mission": execute_mission,
            "bingo": execute_bingo,
            "time": execute_time,
            "index": execute_index,
            "aerodrome": execute_aerodrome,
            "scratchpad": execute_scratchpad
        }

        handlers.get(args.command)(d, args)


if __name__ == "__main__":
    main(sys.argv[1:])
