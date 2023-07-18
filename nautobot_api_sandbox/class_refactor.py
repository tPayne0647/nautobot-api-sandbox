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
    
    def show_sites(self):
        sites_url = self.base_url + "dcim/sites/"
        data = self._get(sites_url)
        sites = [site["name"] for site in data["results"]]
        print(f"\nTotal sites: {len(sites)}\n \n{sites}")
        return sites