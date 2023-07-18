from unittest.mock import MagicMock
import pytest
from nautobot_api_sandbox.nauto_demo_functions import DemoNautobotClient


# Mock Site class
class MockSite:
    def __init__(self, name):
        self.name = name


class MockDevice:
    def __init__(self, name):
        self.name = name


@pytest.fixture
def mock_api():
    mock_api = MagicMock()

    # Mock the Sites API response
    mock_api.dcim.sites.all.return_value = [
        MockSite(name="site1"),
        MockSite(name="site2"),
        MockSite(name="site3"),
    ]

    # Mock the Devices API response
    mock_api.dcim.devices.filter.return_value = [
        MockDevice(name="device1"),
        MockDevice(name="device2"),
        MockDevice(name="device3"),
    ]

    return mock_api


@pytest.fixture
def mock_token():
    return "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


@pytest.fixture
def client(mock_api, mock_token):
    return DemoNautobotClient(api_token=mock_token, api=mock_api)


def test_show_sites(client, mock_api, capfd):
    # Call the function
    client.show_sites()

    # Capture the output
    out, err = capfd.readouterr()

    # Check the output
    assert "Total sites: 3" in out
    assert "site1" in out
    assert "site2" in out
    assert "site3" in out


def test_show_devices(client, mock_api, capfd):
    # Call the function
    client.show_devices(selected_site="site1")

    # Capture the output
    out, err = capfd.readouterr()

    # Check the output
    assert "Total number of devices in [SITE1]: 3" in out
    assert "device1" in out
    assert "device2" in out
    assert "device3" in out
