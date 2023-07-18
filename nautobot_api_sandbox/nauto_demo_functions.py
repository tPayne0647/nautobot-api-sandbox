import requests
import json


# Nautobot Demo API sandbox

# Demo URLs and Token
base_url = "https://demo.nautobot.com/api/"
sites_url = base_url + "dcim/sites/"
devices_url = base_url + "dcim/devices/"
tenant_url = base_url + "tenancy/tenants/"
api_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Set Headers
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization": f"Token {api_token}",
}


def show_sites():
    global sites
    data = requests.get(sites_url,headers=headers,)
    sites_data = data.json()

    sites = [site["name"] for site in sites_data["results"]]
    total_sites = len(sites)
    print(f"\nTotal sites: {total_sites}\n \n{sites}")
    return sites


def show_devices(selected_site):
    test_parameters = {"site": selected_site}
    device_data = requests.get(
        devices_url,
        headers=headers,
        params=test_parameters,
    )
    name_list = device_data.json()
    device_names = [device["name"] for device in name_list["results"]]
    total_devices = len(device_names)

    print(f"\nTotal number of devices in [{selected_site.upper()}]: {total_devices}\n\n{device_names}")
    return total_devices
    


tenant_id = ""


def create_tenant(name):
    global tenant_id
    data = {
        "name": name,
    }
    response = requests.post(tenant_url, headers=headers, data=json.dumps(data))

    if response.status_code == 201:
        print("Tenant created successfully.\n")
        tenant_id = response.json().get("id")
        return response.json()
    else:
        print("Failed to create tenant. Response:", response.content)
        return None


def get_tenant_id(name):
    response = requests.get(tenant_url, headers=headers)

    if response.status_code == 200:
        tenants = response.json()["results"]
        for tenant in tenants:
            if tenant["name"] == name:
                print(tenant["id"])
                return tenant["id"]
        print(f"Tenant with name '{name}' not found.")
        return None
    else:
        print(f"Failed to get tenants. Response: {response.content}")
        return None


def delete_tenant(name):
    tenant_id = get_tenant_id(name)
    if tenant_id is None:
        return 

    delete_tenant_url = tenant_url + tenant_id
    response = requests.delete(delete_tenant_url, headers=headers)

    if response.status_code == 204:
        print(f"Tenant [{name}] deleted successfully!")
    else:
        print(f"ERROR! Tenant [{name}] could not be deleted")


def show_tenants():
    tenant_data = requests.get(tenant_url, headers=headers)
    name_list = tenant_data.json()
    tenant_names = [tenant["name"] for tenant in name_list["results"]]

    print(f"\nTotal tenants: {len(tenant_names)}\n \n{tenant_names}")
    return tenant_names