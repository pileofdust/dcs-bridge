from dcsbridge.dataloaders.scratchpad import ScratchpadDataLoader as DataLoader


def test_load_single_coordinate():
    """
    GIVEN A DCS Scratchpad datafile with a single coordinate
    WHEN the class is instantiated and method is called
    THEN load into current selected steerpoint
    """

    dataloader = DataLoader("test/resources/TestData-Single-0000.txt")
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

    dataloader = DataLoader("test/resources/TestData-Single-CMD-0000.txt")
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
    WHEN the class is instantiated and methos is called
    THEN load into steerpoint according to index and commands
    """

    dataloader = DataLoader("test/resources/TestData-Multiple-Complex-0000.txt")
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
