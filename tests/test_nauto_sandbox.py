"""
Module for testing Nautobot API Sandbox
"""

from unittest.mock import MagicMock
import pytest
from nautobot_api_sandbox.nauto_demo_functions import (
    DemoNautobotClient,
    TenantNotFoundError,
)


@pytest.fixture
def mock_api():
    """
    Mock API fixture for testing.
    """
    mock_api = MagicMock()

    # Mock the Sites API response
    site1 = MagicMock(name="site1")
    site1.name = "site1"
    site2 = MagicMock(name="site2")
    site2.name = "site2"
    site3 = MagicMock(name="site3")
    site3.name = "site3"
    mock_api.dcim.sites.all.return_value = [site1, site2, site3]

    # Mock the Devices API response
    device1 = MagicMock(name="device1")
    device1.name = "device1"
    device2 = MagicMock(name="device2")
    device2.name = "device2"
    device3 = MagicMock(name="device3")
    device3.name = "device3"
    mock_api.dcim.devices.filter.return_value = [device1, device2, device3]

    return mock_api


@pytest.fixture
def mock_token():
    """
    Mock API token fixture for testing.
    """
    return "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"


@pytest.fixture
def client(mock_api, mock_token):
    """
    Nautobot API client fixture for testing.
    """
    return DemoNautobotClient(api_token=mock_token, api=mock_api)


def test_show_sites(client, mock_api):
    """
    Test case for showing sites.
    """
    sites = client.get_sites()
    assert len(sites) == 3
    assert sites[0].name == "site1"
    assert sites[1].name == "site2"
    assert sites[2].name == "site3"


def test_show_devices(client, mock_api):
    """
    Test case for showing devices.
    """
    devices = client.get_devices(selected_site_name="site1")
    assert len(devices) == 3
    assert devices[0].name == "device1"
    assert devices[1].name == "device2"
    assert devices[2].name == "device3"


def test_create_tenant(client, mock_api):
    """
    Test case for creating a tenant.
    """
    mock_tenant = MagicMock()
    mock_api.tenancy.tenants.create.return_value = mock_tenant
    tenant = client.create_tenant(name="Test Tenant")
    assert tenant == mock_tenant


def test_get_tenant_existing(client, mock_api):
    """
    Test case for getting an existing tenant.
    """
    mock_tenant = MagicMock()
    mock_tenant.name = "Test Tenant"
    mock_tenant.id = 123
    mock_api.tenancy.tenants.get.return_value = mock_tenant
    tenant = client.get_tenant(name="Test Tenant")
    assert tenant.id == 123
    assert tenant == mock_tenant
    mock_api.tenancy.tenants.get.assert_called_once_with(name="Test Tenant")


def test_get_tenant_nonexistent(client, mock_api):
    """
    Test case for getting a nonexistent tenant.
    """
    mock_api.tenancy.tenants.get.return_value = None
    with pytest.raises(TenantNotFoundError):
        client.get_tenant(name="Nonexistent Tenant")
    mock_api.tenancy.tenants.get.assert_called_with(name="Nonexistent Tenant")


def test_delete_tenant_existing(client, mock_api):
    """
    Test case for deleting an existing tenant.
    """
    mock_tenant = MagicMock()
    mock_tenant.name = "Test Tenant"
    mock_api.tenancy.tenants.get.return_value = mock_tenant
    client.delete_tenant(name="Test Tenant")
    mock_api.tenancy.tenants.get.assert_called_once_with(name="Test Tenant")
    mock_tenant.delete.assert_called_once()


def test_delete_tenant_nonexistent(client, mock_api):
    """
    Test case for deleting a nonexistent tenant.
    """
    mock_api.tenancy.tenants.get.return_value = None
    with pytest.raises(TenantNotFoundError):
        client.delete_tenant(name="Nonexistent Tenant")
    mock_api.tenancy.tenants.get.assert_called_with(name="Nonexistent Tenant")
