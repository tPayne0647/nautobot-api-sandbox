"""
Module for testing Nautobot API Sandbox
"""

from unittest.mock import MagicMock, Mock
import pytest
import pynautobot
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


class TestDemoNautobotClient:
    @pytest.fixture(autouse=True)
    def setup(self, mock_api, mock_token):
        self.client = DemoNautobotClient(api_token=mock_token, api=mock_api)
        self.mock_api = mock_api

    def test_get_sites(self):
        sites = self.client.get_sites()
        assert len(sites) == 3
        assert sites[0].name == "site1"
        assert sites[1].name == "site2"
        assert sites[2].name == "site3"
        self.mock_api.dcim.sites.all.assert_called_once()

    def test_get_sites_no_sites(self):
        self.mock_api.dcim.sites.all.return_value = []
        sites = self.client.get_sites()
        assert sites == []

    def test_get_devices_no_devices(self):
        self.mock_api.dcim.devices.filter.return_value = []
        devices = self.client.get_devices(selected_site_name="site1")
        assert devices == []

    def test_get_devices(self):
        devices = self.client.get_devices(selected_site_name="site1")
        assert len(devices) == 3
        assert devices[0].name == "device1"
        assert devices[1].name == "device2"
        assert devices[2].name == "device3"

    def test_create_tenant(self):
        mock_tenant = MagicMock()
        self.mock_api.tenancy.tenants.create.return_value = mock_tenant
        tenant = self.client.create_tenant(name="Test Tenant")
        assert tenant == mock_tenant

    def test_create_existing_tenant(self):
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.reason = "A tenant with this name already exists."
        self.mock_api.tenancy.tenants.create.side_effect = pynautobot.core.query.RequestError(
            mock_response
        )
        tenant = self.client.create_tenant(name="Test Tenant")
        assert tenant is None

    def test_get_tenant_existing(self):
        mock_tenant = MagicMock()
        mock_tenant.name = "Test Tenant"
        mock_tenant.id = 123
        self.mock_api.tenancy.tenants.get.return_value = mock_tenant
        tenant = self.client.get_tenant(name="Test Tenant")
        assert tenant.id == 123
        assert tenant == mock_tenant
        self.mock_api.tenancy.tenants.get.assert_called_once_with(name="Test Tenant")

    def test_delete_tenant_existing(self):
        mock_tenant = MagicMock()
        mock_tenant.name = "Test Tenant"
        self.mock_api.tenancy.tenants.get.return_value = mock_tenant
        self.client.delete_tenant(name="Test Tenant")
        self.mock_api.tenancy.tenants.get.assert_called_once_with(name="Test Tenant")
        mock_tenant.delete.assert_called_once()

    def test_delete_tenant_nonexistent(self):
        self.mock_api.tenancy.tenants.get.return_value = None
        with pytest.raises(TenantNotFoundError):
            self.client.delete_tenant("Nonexistent Tenant")

    def test_delete_tenant_dependant(self):
        mock_tenant = MagicMock()
        mock_response = Mock()
        mock_response.status_code = 409
        mock_response.text = (
            "The request failed with code 409 Conflict: "
            "{'detail': 'Unable to delete object. 1 dependent objects were found: Policy 3 (88f1ce52-bd40-4780-95de-381c8ed14bc0)'}"
        )
        mock_tenant.delete.side_effect = pynautobot.core.query.RequestError(mock_response)
        self.mock_api.tenancy.tenants.get.return_value = mock_tenant
        success, message = self.client.delete_tenant(name="Test Tenant")
        assert not success
