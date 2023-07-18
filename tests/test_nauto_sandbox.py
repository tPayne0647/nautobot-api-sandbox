from unittest.mock import MagicMock
import pytest
from nautobot_api_sandbox.nauto_demo_functions import DemoNautobotClient


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


def test_create_tenant(client, mock_api, capfd):
    # Mock the tenant creation
    mock_tenant = MagicMock()
    mock_api.tenancy.tenants.create.return_value = mock_tenant

    # Call the function
    client.create_tenant(name="Test Tenant")

    # Capture the output
    out, err = capfd.readouterr()

    # Check the output
    assert "Tenant created successfully." in out


def test_get_tenant_existing(client, mock_api, capfd):
    # Mock the tenant retrieval
    mock_tenant = MagicMock()
    mock_tenant.name = "Test Tenant"
    mock_tenant.id = 123
    mock_api.tenancy.tenants.get.return_value = mock_tenant

    # Call the function with an existing tenant name
    tenant = client.get_tenant(name="Test Tenant")

    # Capture the output
    out, err = capfd.readouterr()

    # Check the output and return value
    assert out.strip() == "123"  # Check if the ID is printed
    assert tenant == mock_tenant
    mock_api.tenancy.tenants.get.assert_called_once_with(name="Test Tenant")


def test_get_tenant_nonexistent(client, mock_api, capfd):
    # Mock the tenant retrieval
    mock_api.tenancy.tenants.get.return_value = None

    # Call the function with a non-existent tenant name
    client.get_tenant(name="Nonexistent Tenant")

    # Capture the output
    out, err = capfd.readouterr()

    # Check the output
    assert out.strip() == "Tenant with name 'Nonexistent Tenant' not found."
    mock_api.tenancy.tenants.get.assert_called_with(name="Nonexistent Tenant")


def test_delete_tenant_existing(client, mock_api, capfd):
    # Mock the tenant retrieval
    mock_tenant = MagicMock()
    mock_tenant.name = "Test Tenant"
    mock_api.tenancy.tenants.get.return_value = mock_tenant

    # Call the function with an existing tenant name
    client.delete_tenant(name="Test Tenant")

    # Capture the output
    out, err = capfd.readouterr()

    # Check the output
    expected_output = f"Tenant [{mock_tenant.name}] deleted successfully!"
    assert expected_output in out.strip()
    mock_api.tenancy.tenants.get.assert_called_once_with(name="Test Tenant")
    mock_tenant.delete.assert_called_once()


def test_delete_tenant_nonexistent(client, mock_api, capfd):
    # Mock the tenant retrieval
    mock_api.tenancy.tenants.get.return_value = None

    # Call the function with a non-existent tenant name
    client.delete_tenant(name="Nonexistent Tenant")

    # Capture the output
    out, err = capfd.readouterr()

    # Check the output
    expected_output = "Tenant with name 'Nonexistent Tenant' not found."
    assert expected_output in out.strip()
    mock_api.tenancy.tenants.get.assert_called_with(name="Nonexistent Tenant")
