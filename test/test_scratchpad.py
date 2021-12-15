from dcsbridge.dataloaders.scratchpad import ScratchpadDataLoader as DataLoader
from importlib.resources import files


def test_load_single_coordinate():
    """
    GIVEN A DCS Scratchpad datafile with a single coordinate
    WHEN the class is instantiated and method is called
    THEN load into current selected steerpoint
    """

    datafile = files("test.resources").joinpath("TestData-Single-0000.txt")
    dataloader = DataLoader(datafile)
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    assert waypoints is not None
    assert len(waypoints) == 1

    lat, lon, alt = waypoints[1]
    assert lat is not None
    assert lon is not None
    assert alt is not None

    assert lat == "N3747332"
    assert lon == "W11425693"
    assert alt == "4913"


def test_load_single_coordinate_with_command():
    """
    GIVEN A DCS Scratchpad datafile with a single coordinate preceded with a command statement
    WHEN the class is instantiated and method is called
    THEN load into steerpoint with index from commmand
    """

    datafile = files("test.resources").joinpath("TestData-Single-CMD-0000.txt")
    dataloader = DataLoader(datafile)
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    assert waypoints is not None
    assert len(waypoints) == 1

    assert waypoints[82] is not None

    wp = waypoints[82]
    assert wp is not None

    lat, lon, alt = wp
    assert lat is not None
    assert lon is not None
    assert alt is not None

    assert lat == "N3807862"
    assert lon == "W01343181"
    assert alt == "6500"


def test_load_multiple_complex():
    """
    GIVEN A DCS Scratchpad datafile with multiple coordinates and commands
    WHEN the class is instantiated and method is called
    THEN load into steerpoint according to index and commands
    """

    datafile = files("test.resources").joinpath("TestData-Multiple-Complex-0000.txt")
    dataloader = DataLoader(datafile)
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    assert waypoints is not None
    assert type(waypoints) is dict
    assert len(waypoints) == 6

    assert waypoints[1] is not None
    assert waypoints[2] is not None
    assert waypoints[3] is not None
    assert waypoints[4] is not None
    assert waypoints[5] is not None
    assert waypoints[81] is not None


def test_load_multiple_complex_with_bingo():
    """
    GIVEN A DCS Scratchpad datafile with multiple coordinates and commands
    WHEN the class is instantiated and method is called
    THEN load steerpoint and bingo setting
    """

    datafile = files("test.resources").joinpath("TestData-Multiple-Complex-With-Bingo-0000.txt")
    dataloader = DataLoader(datafile)
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    assert waypoints is not None
    assert type(waypoints) is dict
    assert len(waypoints) == 6

    bingo = dataloader.get_bingo()
    assert bingo is not None
    assert bingo == "4530"


def test_load_multiple_formats():
    """
    GIVEN A DCS Scratchpad datafile with steerpoint with coordinates in multiple different formats
    WHEN the class is instantiated and method is called
    THEN load steerpoint DDM coordinates
    """

    datafile = files("test.resources").joinpath("TestData-Scratchpad-Multiple-Formats.txt")
    dataloader = DataLoader(datafile)
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    assert waypoints is not None
    assert type(waypoints) is dict
    assert len(waypoints) == 1

    assert waypoints[1] is not None

    wp = waypoints[1]
    assert wp is not None

    lat, lon, alt = wp
    assert lat is not None
    assert lon is not None
    assert alt is not None

    assert lat == "N3747332"
    assert lon == "W11425693"
    assert alt == "4913"


def test_load_steerpoint_without_altitude_in_meters():
    """
    GIVEN A DCS Scratchpad datafile with steerpoint where altitude only in feet
    WHEN the class is instantiated and method is called
    THEN load steerpoint DDM coordinates and elevation in feet
    """

    datafile = files("test.resources").joinpath("TestData-Scratchpad-No-Meter.txt")
    dataloader = DataLoader(datafile)
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    assert waypoints is not None
    assert type(waypoints) is dict
    assert len(waypoints) == 1

    assert waypoints[1] is not None

    wp = waypoints[1]
    assert wp is not None

    lat, lon, alt = wp
    assert lat is not None
    assert lon is not None
    assert alt is not None

    assert lat == "N3747332"
    assert lon == "W11425693"
    assert alt == "152"


def test_load_scratchpad_with_aerodrome_command():
    """
    GIVEN A DCS Scratchpad datafile with aerodrome command
    WHEN the class is instantiated and method is called
    THEN load steerpoint coordinates from aerodrome file
    """

    datafile = files("test.resources").joinpath("TestData-Scratchpad-Aerodrome.txt")
    dataloader = DataLoader(datafile)
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    assert waypoints is not None
    assert type(waypoints) is dict
    assert len(waypoints) == 6

    assert waypoints[1] is not None
    wp = waypoints[1]
    assert wp is not None

    lat, lon, alt = wp
    assert lat is not None
    assert lon is not None
    assert alt is not None

    assert lat == "N3232350"
    assert lon == "E03811700"
    assert alt == "2257"

    assert waypoints[20] is not None
    wp = waypoints[20]
    assert wp is not None

    lat, lon, alt = wp
    assert lat is not None
    assert lon is not None
    assert alt is not None

    assert lat == "N3714000"
    assert lon == "W11547533"
    assert alt == "4495"
