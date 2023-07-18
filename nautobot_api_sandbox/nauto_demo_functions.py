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
        self.logger.addHandler(logging.StreamHandler())  # Outputs log messages to the console
        self.logger.setLevel(logging.INFO)  # Set the desired log level

    def get_sites(self):
        """Return a list of all sites."""
        return self.api.dcim.sites.all()

    def display_sites(self):
        """Display the names of all sites."""
        sites = self.get_sites()
        self.logger.info(f"\nTotal sites: {len(sites)}\n \n{[site.name for site in sites]}")

    def get_devices(self, selected_site):
        """Return a list of all devices at the specified site, or raise SiteNotFoundError if the site does not exist."""
        try:
            devices = self.api.dcim.devices.filter(site=selected_site)
        except RequestError as request_error:
            if "is not one of the available choices" in str(request_error):
                raise SiteNotFoundError(f"Site '{selected_site}' not found.") from request_error
            raise request_error
        if not devices:
            raise SiteNotFoundError(f"Site '{selected_site}' not found.")
        return devices

    def display_devices(self, selected_site):
        """Display the names of all devices at the specified site."""
        devices = self.get_devices(selected_site)
        self.logger.info(
            f"\nTotal number of devices in [{selected_site.upper()}]: {len(devices)}\n\n{[device.name for device in devices]}"
        )

    def create_tenant(self, name):
        """Create a new tenant with the specified name and return it."""
        tenant = self.api.tenancy.tenants.create(name=name)
        self.logger.info(f"Tenant '{name}' created successfully.\n")
        return tenant

    def get_tenant(self, name):
        """Return the tenant with the specified name, or raise TenantNotFoundError if the tenant does not exist."""
        tenant = self.api.tenancy.tenants.get(name=name)
        if tenant is None:
            raise TenantNotFoundError(f"Tenant with name '{name}' not found.")
        return tenant

    def delete_tenant(self, name):
        """Delete the tenant with the specified name."""
        tenant = self.get_tenant(name)
        if tenant is not None:
            tenant.delete()
            self.logger.info(f"Tenant '{name}' deleted successfully!")
        else:
            raise TenantNotFoundError(f"Tenant with name '{name}' not found.")

    def get_tenants(self):
        """Return a list of all tenants."""
        return self.api.tenancy.tenants.all()

    def display_tenants(self):
        """Display the names of all tenants."""
        tenants = self.get_tenants()
        self.logger.info(
            f"\nTotal tenants: {len(tenants)}\n \n{[tenant.name for tenant in tenants]}"
        )
