from dcsbridge.dataloaders.file import ExcelDataLoader
from dcsbridge.dataloaders.file import TextFileDataLoader


def test_load_minimum_excel():
    """
    GIVEN A data file in Excel with the three minimum columns
    WHEN the class is created and data is loaded
    THEN waypoint are loaded and can be retrieved as a dictionary or individual by index
    """

    dataloader = ExcelDataLoader("tests/resources/TestData-Minimum.xlsx")
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    check_waypoints(waypoints)

    for wp in waypoints.values():
        lat, lon, alt = wp
        assert lat is not None
        assert lon is not None
        assert alt is not None

    wp1 = dataloader.get_waypoint("1")
    assert wp1 is not None
    assert wp1 is waypoints["1"]
    check_waypoint(wp1)


def test_load_minimum_text_file():
    """
    GIVEN A delimited text file with the three minimum columns
    WHEN the class is created and data is loaded
    THEN waypoint are loaded and can be retrieved as a dictionary or individual by index
    """

    dataloader = TextFileDataLoader("tests/resources/TestData-Minimum.csv")
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    check_waypoints(waypoints)

    for wp in waypoints.values():
        lat, lon, alt = wp
        assert lat is not None
        assert lon is not None
        assert alt is not None

    wp1 = dataloader.get_waypoint("1")
    assert wp1 is not None
    assert wp1 is waypoints["1"]
    check_waypoint(wp1)


def test_load_text_file_with_column_specification():
    """
    GIVEN A delimited text file with more than minimum columns
    WHEN the class is created, columns are specified and data is loaded
    THEN waypoint are loaded and can be retrieved as a dictionary or individual by index
    """

    dataloader = TextFileDataLoader("tests/resources/TestData-Columns.csv", columns="1,3,5")
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    check_waypoints(waypoints)

    wp1 = dataloader.get_waypoint("1")
    assert wp1 is not None
    assert wp1 is waypoints["1"]
    check_waypoint(wp1)


def check_waypoints(waypoints):
    assert waypoints is not None
    assert len(waypoints) == 10

    for wp in waypoints.values():
        lat, lon, alt = wp
        assert lat is not None
        assert lon is not None
        assert alt is not None


def check_waypoint(waypoint):
    lat, lon, alt = waypoint
    assert lat == "N3543883"
    assert lon == "E03707117"
    assert alt == "820"
