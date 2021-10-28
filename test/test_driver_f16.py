import pytest
import re
from collections import namedtuple
from dcsbridge.drivers.f16 import Driver


class Writer:
    def __init__(self):
        self.__result = []

    def send(self, msg):
        self.__result.append(msg)

    def get_result(self):
        return self.__result

    def reset(self):
        self.__result = []


__icp_pattern = re.compile(r"LIST|ENTR|RCL")
__icp_btn_pattern = re.compile(r"0|1|2|3|4|5|6|7|8|9")


def play(seq, result):
    i = 0
    for v in seq:
        btnPress = None
        btnRelease = None
        if __icp_pattern.match(v):
            btnPress = f"ICP_{v}_BTN 1\n"
            btnRelease = f"ICP_{v}_BTN 0\n"
        elif __icp_btn_pattern.match(v):
            btnPress = f"ICP_BTN_{v} 1\n"
            btnRelease = f"ICP_BTN_{v} 0\n"
        elif "UP" == v:
            btnPress = "ICP_DATA_UP_DN_SW 2\n"
            btnRelease = "ICP_DATA_UP_DN_SW 1\n"
        elif "DOWN" == v:
            btnPress = "ICP_DATA_UP_DN_SW 0\n"
            btnRelease = "ICP_DATA_UP_DN_SW 1\n"
        elif "LEFT" == v:
            btnPress = "ICP_DATA_RTN_SEQ_SW 0\n"
            btnRelease = "ICP_DATA_RTN_SEQ_SW 1\n"
        elif "RIGHT" == v:
            btnPress = "ICP_DATA_RTN_SEQ_SW 2\n"
            btnRelease = "ICP_DATA_RTN_SEQ_SW 1\n"
        else:
            raise Exception(f"Unknown sequence: {v}")

        assert btnPress == result[i]
        assert btnRelease == result[i + 1]

        i = i + 2


@pytest.fixture
def context():
    tw = Writer()
    driver = Driver(tw, 0.0, 0.0)

    return (driver, tw)


def test_set_bullseye(context):
    """
    GIVEN Coordinates for Bullseye
    WHEN the execute method is called
    THEN the correct sequence for the bullseye steerpoint is entered
    """

    driver, tw = context
    driver.enter_bullseye(None)

    assert len(tw.get_result()) == 0


def test_set_bingo(context):
    """
    GIVEN Amount for Bingo fuel
    WHEN  the execute method is called
    THEN the correct sequence for setting bingo is entered
    """

    driver, tw = context
    value = "2345"
    seq = ["LEFT", "LIST", "2", "2", "3", "4", "5", "ENTR", "LEFT"]
    driver.enter_bingo(value)
    play(seq, tw.get_result())


def test_set_steerpoint(context):
    """
    GIVEN Coordinates for steerpoint
    WHEN the steerpoint is already selected and the execute method is called
    THEN the correct sequence for the steerpoint is entered
    """

    driver, tw = context

    lat = "N3534567"
    lon = "E14554243"
    alt = "548"

    seq = [
        "DOWN",
        "DOWN",
        "2",
        "3",
        "5",
        "3",
        "4",
        "5",
        "6",
        "7",
        "ENTR",
        "DOWN",
        "6",
        "1",
        "4",
        "5",
        "5",
        "4",
        "2",
        "4",
        "3",
        "ENTR",
        "DOWN",
        "5",
        "4",
        "8",
        "ENTR",
        "UP",
        "UP",
        "UP",
        "UP",
    ]
    driver.enter_steerpoint((lat, lon, alt))
    play(seq, tw.get_result())

    """
  GIVEN Coordinates for steerpoint
  WHEN the steerpoint index is provided and the execute method is called
  THEN the correct sequence for the steerpoint is entered
  """

    tw.reset()

    index = "18"
    seq = ["1", "8", "ENTR"] + seq
    driver.enter_steerpoint((lat, lon, alt), index)
    play(seq, tw.get_result())


def test_set_steerpoints(context):
    """
    GIVEN List of coordinates for steerpoints
    WHEN the list is privided and the execute method is called
    THEN the steerpoint screen is entered and the correct sequence for the steerpoint is entered and the first steerpoint is selected
    """

    driver, tw = context

    seq = ["LEFT", "4", "1", "ENTR"]
    lat1 = "S3534567"
    lon1 = "W14554243"
    alt1 = "548"
    sp1 = (lat1, lon1, alt1)

    seq = seq + [
        "DOWN",
        "DOWN",
        "8",
        "3",
        "5",
        "3",
        "4",
        "5",
        "6",
        "7",
        "ENTR",
        "DOWN",
        "4",
        "1",
        "4",
        "5",
        "5",
        "4",
        "2",
        "4",
        "3",
        "ENTR",
        "DOWN",
        "5",
        "4",
        "8",
        "ENTR",
        "UP",
        "UP",
        "UP",
        "UP",
    ]

    lat2 = "N3742264"
    lon2 = "E04554599"
    alt2 = "14548"
    sp2 = (lat2, lon2, alt2)

    seq = seq + [
        "2",
        "ENTR",
        "DOWN",
        "DOWN",
        "2",
        "3",
        "7",
        "4",
        "2",
        "2",
        "6",
        "4",
        "ENTR",
        "DOWN",
        "6",
        "0",
        "4",
        "5",
        "5",
        "4",
        "5",
        "9",
        "9",
        "ENTR",
        "DOWN",
        "1",
        "4",
        "5",
        "4",
        "8",
        "ENTR",
        "UP",
        "UP",
        "UP",
        "UP",
        "1",
        "ENTR",
        "LEFT",
    ]

    driver.enter_steerpoints([sp1, sp2])
    play(seq, tw.get_result())


def test_set_time(context):
    """
    GIVEN Time object is given
    WHEN the execute command is called
    THEN the correct sequence is entered to bring up the time screen and set the system clock to the given time
    """

    driver, tw = context

    test_time_struct = namedtuple(
        'test_time_struct', ['tm_hour', 'tm_min', 'tm_sec'])

    time = test_time_struct(11, 40, 17)

    seq = ["LEFT", "6", "1", "1", "4", "0", "1", "7", "ENTR", "LEFT"]
    driver.enter_time(time)
    play(seq, tw.get_result())

    tw.reset()

    # Time with leading zero in seconds
    time = test_time_struct(11, 40, 7)

    seq = ["LEFT", "6", "1", "1", "4", "0", "0", "7", "ENTR", "LEFT"]
    driver.enter_time(time)
    play(seq, tw.get_result())

def test_set_steerpoints_with_position(context):
    """
    GIVEN List of coordinates for steerpoints
    WHEN the list is provided and the execute method is called
    THEN the steerpoint screen is entered and the correct sequence for the steerpoint is
        entered in the corresponding position and the first steerpoint in the list is selected
    """

    driver, tw = context

    seq = ["LEFT", "4", "8", "2", "ENTR"]
    lat1 = "N3807862"
    lon1 = "W01343181"
    alt1 = "6500"
    sp1 = (lat1, lon1, alt1)

    seq = seq + [
        "DOWN",
        "DOWN",
        "2",
        "3",
        "8",
        "0",
        "7",
        "8",
        "6",
        "2",
        "ENTR",
        "DOWN",
        "4",
        "0",
        "1",
        "3",
        "4",
        "3",
        "1",
        "8",
        "1",
        "ENTR",
        "DOWN",
        "6",
        "5",
        "0",
        "0",
        "ENTR",
        "UP",
        "UP",
        "UP",
        "UP",
        "8",
        "2",
        "ENTR"
    ]

    steerpoints = {}
    steerpoints[82] = sp1
    driver.enter_steerpoints(steerpoints)
    play(seq, tw.get_result())
