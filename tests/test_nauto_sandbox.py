import pytest
from unittest.mock import MagicMock
from nautobot_api_sandbox.nauto_demo_functions import DemoNautobotClient, TenantNotFoundError


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


def test_show_sites(client, mock_api):
    sites = client.get_sites()
    assert len(sites) == 3
    assert sites[0].name == "site1"
    assert sites[1].name == "site2"
    assert sites[2].name == "site3"


def test_show_devices(client, mock_api):
    devices = client.get_devices(selected_site="site1")
    assert len(devices) == 3
    assert devices[0].name == "device1"
    assert devices[1].name == "device2"
    assert devices[2].name == "device3"


def test_create_tenant(client, mock_api):
    mock_tenant = MagicMock()
    mock_api.tenancy.tenants.create.return_value = mock_tenant
    tenant = client.create_tenant(name="Test Tenant")
    assert tenant == mock_tenant


def test_get_tenant_existing(client, mock_api):
    mock_tenant = MagicMock()
    mock_tenant.name = "Test Tenant"
    mock_tenant.id = 123
    mock_api.tenancy.tenants.get.return_value = mock_tenant
    tenant = client.get_tenant(name="Test Tenant")
    assert tenant.id == 123
    assert tenant == mock_tenant
    mock_api.tenancy.tenants.get.assert_called_once_with(name="Test Tenant")


def test_get_tenant_nonexistent(client, mock_api):
    mock_api.tenancy.tenants.get.return_value = None
    with pytest.raises(TenantNotFoundError):
        client.get_tenant(name="Nonexistent Tenant")
    mock_api.tenancy.tenants.get.assert_called_with(name="Nonexistent Tenant")


def test_delete_tenant_existing(client, mock_api):
    mock_tenant = MagicMock()
    mock_tenant.name = "Test Tenant"
    mock_api.tenancy.tenants.get.return_value = mock_tenant
    client.delete_tenant(name="Test Tenant")
    mock_api.tenancy.tenants.get.assert_called_once_with(name="Test Tenant")
    mock_tenant.delete.assert_called_once()


def test_delete_tenant_nonexistent(client, mock_api):
    mock_api.tenancy.tenants.get.return_value = None
    with pytest.raises(TenantNotFoundError):
        client.delete_tenant(name="Nonexistent Tenant")
    mock_api.tenancy.tenants.get.assert_called_with(name="Nonexistent Tenant")
