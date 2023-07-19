"""Functions module"""

import logging
import pynautobot
from pynautobot.core.query import RequestError


class TenantNotFoundError(Exception):
    """Exception raised when a tenant is not found."""


class SiteNotFoundError(Exception):
    """Exception raised when a site is not found."""


class DemoNautobotClient:
    """A client for interacting with Nautobot."""

    def __init__(self, api_token, api=None):
        """Initialize the client with an API token and an optional pynautobot API object."""
        if api is None:
            self.api = pynautobot.api("https://demo.nautobot.com", token=api_token)
        else:
            self.api = api

        self.logger = logging.getLogger(__name__)
        self.logger.addHandler(
            logging.StreamHandler()
        )  # Outputs log messages to the console
        self.logger.setLevel(logging.INFO)  # Set the desired log level

    def get_sites(self):
        """Return a list of all sites."""
        return self.api.dcim.sites.all()

    def display_sites(self):
        """Display the names of all sites."""
        sites = self.get_sites()
        self.logger.info(
            "\nTotal sites: %s\n \n%s", len(sites), [site.name for site in sites]
        )

    def get_devices(self, selected_site):
        """Return a list of all devices at the specified site, or raise SiteNotFoundError if the site does not exist."""
        try:
            devices = self.api.dcim.devices.filter(site=selected_site)
        except RequestError as request_error:
            if "is not one of the available choices" in str(request_error):
                raise SiteNotFoundError(
                    "Site '%s' not found.", selected_site
                ) from request_error
            raise request_error
        if not devices:
            raise SiteNotFoundError("Site '%s' not found.", selected_site)
        return devices

    def display_devices(self, selected_site):
        """Display the names of all devices at the specified site."""
        devices = self.get_devices(selected_site)
        self.logger.info(
            "\nTotal number of devices in [%s]: %s\n\n%s",
            selected_site.upper(),
            len(devices),
            [device.name for device in devices],
        )

    def create_tenant(self, name):
        """Create a new tenant with the specified name and return it."""
        tenant = self.api.tenancy.tenants.create(name=name)
        self.logger.info("Tenant '%s' created successfully.\n", name)
        return tenant

    def get_tenant(self, name):
        """Return the tenant with the specified name, or raise TenantNotFoundError if the tenant does not exist."""
        tenant = self.api.tenancy.tenants.get(name=name)
        if tenant is None:
            raise TenantNotFoundError("Tenant with name '%s' not found.", name)
        return tenant

    def delete_tenant(self, name):
        """Delete the tenant with the specified name."""
        tenant = self.get_tenant(name)
        if tenant is not None:
            tenant.delete()
            self.logger.info("Tenant '%s' deleted successfully!", name)
        else:
            raise TenantNotFoundError("Tenant with name '%s' not found.", name)

    def get_tenants(self):
        """Return a list of all tenants."""
        return self.api.tenancy.tenants.all()

    def display_tenants(self):
        """Display the names of all tenants."""
        tenants = self.get_tenants()
        self.logger.info(
            "\nTotal tenants: %s\n \n%s",
            len(tenants),
            [tenant.name for tenant in tenants],
        )
