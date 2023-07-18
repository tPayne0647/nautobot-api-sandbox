import pynautobot
from pynautobot.core.query import RequestError


class TenantNotFoundError(Exception):
    pass


class SiteNotFoundError(Exception):
    pass


class DemoNautobotClient:
    def __init__(self, api_token, api=None):
        if api is None:
            self.api = pynautobot.api("https://demo.nautobot.com", token=api_token)
        else:
            self.api = api

    def get_sites(self):
        return self.api.dcim.sites.all()

    def display_sites(self):
        sites = self.get_sites()
        print(f"\nTotal sites: {len(sites)}\n \n{[site.name for site in sites]}")

    def get_devices(self, selected_site):
        try:
            devices = self.api.dcim.devices.filter(site=selected_site)
        except RequestError as e:
            if "is not one of the available choices" in str(e):
                raise SiteNotFoundError(f"Site '{selected_site}' not found.")
            else:
                raise e  # If it's a different RequestError, raise it as is
        if not devices:
            raise SiteNotFoundError(f"Site '{selected_site}' not found.")
        return devices

    def display_devices(self, selected_site):
        devices = self.get_devices(selected_site)
        print(
            f"\nTotal number of devices in [{selected_site.upper()}]: {len(devices)}\n\n{[device.name for device in devices]}"
        )

    def create_tenant(self, name):
        tenant = self.api.tenancy.tenants.create(name=name)
        print(f"Tenant '{name}' created successfully.\n")
        return tenant

    def get_tenant(self, name):
        tenant = self.api.tenancy.tenants.get(name=name)
        if tenant is None:
            raise TenantNotFoundError(f"Tenant with name '{name}' not found.")
        return tenant

    def delete_tenant(self, name):
        tenant = self.get_tenant(name)
        if tenant is not None:
            tenant.delete()
            print(f"Tenant '{name}' deleted successfully!")
        else:
            raise TenantNotFoundError(f"Tenant with name '{name}' not found.")

    def get_tenants(self):
        return self.api.tenancy.tenants.all()

    def display_tenants(self):
        tenants = self.get_tenants()
        print(f"\nTotal tenants: {len(tenants)}\n \n{[tenant.name for tenant in tenants]}")
