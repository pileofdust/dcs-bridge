from dcsbridge.dataloaders.file import ExcelDataLoader
from dcsbridge.dataloaders.file import TextFileDataLoader


def test_load_minimum_excel():
    """
    GIVEN A data file in Excel with the three minimum columns
    WHEN the class is created and data is loaded
    THEN waypoint are loaded and can be retrieved as a dictionary or individual by index
    """

    dataloader = ExcelDataLoader("test/resources/TestData-Minimum.xlsx")
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    assert waypoints is not None
    assert len(waypoints) == 10

    for wp in waypoints.values():
        lat, lon, alt = wp
        assert lat is not None
        assert lon is not None
        assert alt is not None

    wp1 = dataloader.get_waypoint("1")
    assert wp1 is not None
    assert wp1 is waypoints["1"]

    lat, lon, alt = wp1
    assert lat == "N3543883"
    assert lon == "E03707117"
    assert alt == "820"


def test_load_minimum_text_file():
    """
    GIVEN A delimited text file with the three minimum columns
    WHEN the class is created and data is loaded
    THEN waypoint are loaded and can be retrieved as a dictionary or individual by index
    """

    dataloader = TextFileDataLoader("test/resources/TestData-Minimum.csv")
    dataloader.load_data()

    waypoints = dataloader.get_waypoints()
    assert waypoints is not None
    assert len(waypoints) == 10

    for wp in waypoints.values():
        lat, lon, alt = wp
        assert lat is not None
        assert lon is not None
        assert alt is not None

    wp1 = dataloader.get_waypoint("1")
    assert wp1 is not None
    assert wp1 is waypoints["1"]

    lat, lon, alt = wp1
    assert lat == "N3543883"
    assert lon == "E03707117"
    assert alt == "820"
