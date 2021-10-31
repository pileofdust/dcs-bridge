import dcsbridge.__main__
import pytest


def test_parse_args():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        dcsbridge.__main__.parse_arguments(["invalid"])

    assert pytest_wrapped_e.type == SystemExit

    args = dcsbridge.__main__.parse_arguments(["mission", "some file"])
    assert args
    assert args.command == "mission"
    assert args.file == "some file"


class TestDriver():
    executed = False

    def enter_time(self, time):
        self.executed = True


def test_execute_time():
    driver = TestDriver()
    args = dcsbridge.__main__.parse_arguments(["time", "local"])

    dcsbridge.__main__.execute_time(driver, args)

    assert driver.executed
