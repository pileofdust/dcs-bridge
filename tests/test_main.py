import pytest

import dcsbridge.__main__


def test_parse_args():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        dcsbridge.__main__.parse_arguments(["invalid"])

    assert pytest_wrapped_e.type == SystemExit

    args = dcsbridge.__main__.parse_arguments(["mission", "some file"])
    assert args
    assert args.command == "mission"
    assert args.file == "some file"


class TestDriver:
    def __init__(self):
        self.executed = False

    def enter_time(self, time):
        self.executed = True

    def enter_bingo(self, bingo):
        self.executed = True


def test_execute_time():
    driver = TestDriver()
    args = dcsbridge.__main__.parse_arguments(["time", "local"])

    dcsbridge.__main__.execute_time(driver, args)

    assert driver.executed


def test_execute_bingo():
    driver = TestDriver()
    args = dcsbridge.__main__.parse_arguments(["bingo", "6000"])

    dcsbridge.__main__.execute_bingo(driver, args)

    assert driver.executed
