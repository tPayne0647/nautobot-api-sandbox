import requests
import json


class DemoNautobotClient:
    def __init__(self, api_token):
        self.base_url = "https://demo.nautobot.com/api/"
        self.headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Token {api_token}",
    }
    
    
    def _get(self, url, params=None):
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    
    def _post(self, url, data=None):
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    
    def _delete(self, url):
        response = requests.delete(url, headers=self.headers)
        response.raise_for_status()
        return response
    
    
    def show_sites(self):
        sites_url = self.base_url + "dcim/sites/"
        data = self._get(sites_url)
        sites = [site["name"] for site in data["results"]]
        print(f"\nTotal sites: {len(sites)}\n \n{sites}")
        return sites
    
    
    def show_devices(self, selected_site):
        devices_url = self.base_url + "dcim/devices/"
        parameters = {"site": selected_site}
        data = self._get(devices_url, params=parameters)
        total_site_devices = data["count"]
        device_names = [device["name"] for device in data["results"]]

        print(f"\nTotal number of devices in [{selected_site.upper()}]: {total_site_devices}\n\n{device_names}")
        return total_site_devices
    
    
    def create_tenant(self, name):
        tenant_url = self.base_url + "tenancy/tenants/"
        data = {"name": name}
        response = self._post(tenant_url, data=data)
        
        print("Tenant created successfully.\n")
        tenant_id = response.get("id")
        return response
    
    
    def get_tenant_id(self, name):
        tenant_url = self.base_url + "tenancy/tenants/"
        data = self._get(tenant_url)

        tenants = data["results"]
        for tenant in tenants:
            if tenant["name"] == name:
                print(tenant["id"])
                return tenant["id"]

        print(f"Tenant with name '{name}' not found.")
        return None
    
    
    def delete_tenant(self, name):
        tenant_id = self.get_tenant_id(name)
        if tenant_id is None:
            return

        delete_tenant_url = self.base_url + "tenancy/tenants/" + tenant_id
        self._delete(delete_tenant_url)

        print(f"Tenant [{name}] deleted successfully!")
        
        
    def show_tenants(self):
        tenant_url = self.base_url + "tenancy/tenants/"
        data = self._get(tenant_url)

        tenant_names = [tenant["name"] for tenant in data["results"]]

        print(f"\nTotal tenants: {len(tenant_names)}\n \n{tenant_names}")
        return tenant_names