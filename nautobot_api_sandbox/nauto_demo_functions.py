import pynautobot

class DemoNautobotClient:
    def __init__(self, api_token):
        self.api = pynautobot.api("https://demo.nautobot.com", token=api_token)
    
    def show_sites(self):
        sites = self.api.dcim.sites.all()
        print(f"\nTotal sites: {len(sites)}\n \n{[site.name for site in sites]}")
        return sites

    def show_devices(self, selected_site):
        devices = self.api.dcim.devices.filter(site=selected_site)
        print(f"\nTotal number of devices in [{selected_site.upper()}]: {len(devices)}\n\n{[device.name for device in devices]}")
        return devices

    def create_tenant(self, name):
        tenant = self.api.tenancy.tenants.create(name=name)
        print("Tenant created successfully.\n")
        return tenant

    def get_tenant(self, name):
        tenant = self.api.tenancy.tenants.get(name=name)
        if tenant is None:
            print(f"Tenant with name '{name}' not found.")
        else:
            print(tenant.id)
        return tenant

    def delete_tenant(self, name):
        tenant = self.get_tenant(name)
        if tenant is not None:
            tenant.delete()
            print(f"Tenant [{name}] deleted successfully!")

    def show_tenants(self):
        tenants = self.api.tenancy.tenants.all()
        print(f"\nTotal tenants: {len(tenants)}\n \n{[tenant.name for tenant in tenants]}")
        return tenants