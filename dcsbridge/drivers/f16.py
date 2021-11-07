from time import sleep
from enum import Enum


class ICP(str, Enum):
    def __new__(cls, value, press, release):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.press = press
        obj.release = release

        return obj

    BTN_0 = ("0", "ICP_BTN_0 1\n", "ICP_BTN_0 0\n")
    BTN_1 = ("1", "ICP_BTN_1 1\n", "ICP_BTN_1 0\n")
    BTN_2 = ("2", "ICP_BTN_2 1\n", "ICP_BTN_2 0\n")
    BTN_3 = ("3", "ICP_BTN_3 1\n", "ICP_BTN_3 0\n")
    BTN_4 = ("4", "ICP_BTN_4 1\n", "ICP_BTN_4 0\n")
    BTN_5 = ("5", "ICP_BTN_5 1\n", "ICP_BTN_5 0\n")
    BTN_6 = ("6", "ICP_BTN_6 1\n", "ICP_BTN_6 0\n")
    BTN_7 = ("7", "ICP_BTN_7 1\n", "ICP_BTN_7 0\n")
    BTN_8 = ("8", "ICP_BTN_8 1\n", "ICP_BTN_8 0\n")
    BTN_9 = ("9", "ICP_BTN_9 1\n", "ICP_BTN_9 0\n")

    NORTH = ("N", "ICP_BTN_2 1\n", "ICP_BTN_2 0\n")
    SOUTH = ("S", "ICP_BTN_8 1\n", "ICP_BTN_8 0\n")
    EAST = ("E", "ICP_BTN_6 1\n", "ICP_BTN_6 0\n")
    WEST = ("W", "ICP_BTN_4 1\n", "ICP_BTN_4 0\n")

    ENTR = ("ENTR", "ICP_ENTR_BTN 1\n", "ICP_ENTR_BTN 0\n")
    RCL = ("RCL", "ICP_RCL_BTN 1\n", "ICP_RCL_BTN 0\n")
    LIST = ("LIST", "ICP_LIST_BTN 1\n", "ICP_LIST_BTN 0\n")

    LEFT = ("LEFT", "ICP_DATA_RTN_SEQ_SW 0\n", "ICP_DATA_RTN_SEQ_SW 1\n")
    RIGHT = ("RIGHT", "ICP_DATA_RTN_SEQ_SW 2\n", "ICP_DATA_RTN_SEQ_SW 1\n")
    UP = ("UP", "ICP_DATA_UP_DN_SW 2\n", "ICP_DATA_UP_DN_SW 1\n")
    DOWN = ("DOWN", "ICP_DATA_UP_DN_SW 0\n", "ICP_DATA_UP_DN_SW 1\n")


class Driver:

    __navigate_to_start = [ICP.LEFT]
    __navigate_to_steerpoints = [ICP.BTN_4]
    __navigate_to_bingo = [ICP.LIST, ICP.BTN_2]
    __navigate_to_top_of_steerpoint = [ICP.UP, ICP.UP, ICP.UP, ICP.UP]

    def __init__(self, dcsbios, short_delay=0.1, medium_delay=0.2):
        self.__dcsbios = dcsbios

        self.__short_delay = short_delay
        self.__medium_delay = medium_delay

    def __run(self, keys, delay_after=None):
        if not keys:
            return False

        if not delay_after:
            delay_after = self.__medium_delay

        for key in keys:
            self.__dcsbios.send(key.press)
            sleep(self.__short_delay)

            self.__dcsbios.send(key.release)
            sleep(delay_after)

        return True

    def __encode(self, string):
        seq = []
        for i in range(0, len(string)):
            seq.append(ICP(string[i]))
        return seq

    def __navigate_to_bullseye(self):
        pass

    #
    # Public fuctions
    #

    def enter_steerpoint(self, sp, index:str=None):
        s = []
        if index:
            s += self.__encode(index)
            s.append(ICP.ENTR)

        s.append(ICP.DOWN)

        for string in sp:
            s.append(ICP.DOWN)
            s += self.__encode(string[:9])
            s.append((ICP.ENTR))

        s += self.__navigate_to_top_of_steerpoint
        self.__run(s)

    def enter_steerpoints(self, sps):
        if sps is None or len(sps) == 0:
            return

        self.__run(self.__navigate_to_start)
        self.__run(self.__navigate_to_steerpoints)

        set_steerpoint_seq = [ICP.BTN_1, ICP.ENTR]

        if type(sps) is list:
            for i, sp in enumerate(sps):
                self.enter_steerpoint(sp, str(i+1))
        elif type(sps) is dict:
            keys = sorted(sps.keys())
            for key in keys:
                self.enter_steerpoint(sps[key], str(key))

            set_steerpoint_seq = self.__encode(str(keys[0]))
            set_steerpoint_seq.append(ICP.ENTR)

        # Set first steerpoint
        self.__run(set_steerpoint_seq + self.__navigate_to_start)

    def enter_bingo(self, bingo):
        s = []
        s += self.__navigate_to_start
        s += self.__navigate_to_bingo
        s += self.__encode(bingo)
        s.append(ICP.ENTR)
        s += self.__navigate_to_start

        self.__run(s)

    def enter_time(self, time):
        s = []
        s += self.__navigate_to_start
        s.append(ICP.BTN_6)
        s += self.__encode(f"{time.tm_hour:02d}{time.tm_min:02d}{time.tm_sec:02d}")
        s.append(ICP.ENTR)
        s += self.__navigate_to_start

        self.__run(s)

    def enter_bullseye(self, sp):
        self.__navigate_to_bullseye()
