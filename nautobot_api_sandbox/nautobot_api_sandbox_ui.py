"""This is the command line interface for the Nautobot API Sandbox."""

from nautobot_api_sandbox.nauto_demo_functions import (
    DemoNautobotClient,
    TenantNotFoundError,
    SiteNotFoundError,
)

WELCOME_MSG = """
Welcome to tPayne's nautobot demo API sandbox!
********************************************************************************
Here is a list of available commands:
show_sites.............................Get list of all sites
show_devices [SITE NAME]...............Get count of devices and list device names
create_tenant [TENANT NAME]............Create a new tenant with specified name
get_tenant [TENANT NAME]...............Get specified tenant
delete_tenant [TENANT NAME]............Delete specified tenant
show_tenants...........................Get count and list all tenant names
help...................................Reprint this window
********************************************************************************
"""


def user_interface():
    """Run the user interface for interacting with the Nautobot API."""
    api_token = input("Please enter your API token: ")
    nautobot_client = DemoNautobotClient(api_token=api_token)
    print(WELCOME_MSG)

    # Commands that need an argument
    commands_with_arg = ["show_devices", "create_tenant", "delete_tenant", "get_tenant"]

    while True:
        command_input = input("Enter a command: ").split(" ", 1)
        command = command_input[0]

        # Check if the command needs an argument and if it was provided
        if command in commands_with_arg:
            if len(command_input) == 1:
                print(f"The {command} command requires an argument.")
                continue
            arg = command_input[1].strip()

        if command == "show_sites":
            nautobot_client.display_sites()
        elif command == "show_devices":
            try:
                nautobot_client.display_devices(arg)
            except SiteNotFoundError:
                print(f"Site '{arg}' not found. Please enter a valid site name.")

        elif command == "create_tenant":
            nautobot_client.create_tenant(arg)
        elif command == "delete_tenant":
            try:
                nautobot_client.delete_tenant(arg)
            except TenantNotFoundError:
                print(f"Tenant '{arg}' not found. Please enter a valid tenant name.")
        elif command == "show_tenants":
            nautobot_client.display_tenants()
        elif command == "get_tenant":
            try:
                tenant = nautobot_client.get_tenant(arg)
                if tenant is not None:
                    print(f"Tenant ID: {tenant.id}\nTenant Name: {tenant.name}")
            except TenantNotFoundError:
                print(f"Tenant '{arg}' not found. Please enter a valid tenant name.")
        elif command == "help":
            print(WELCOME_MSG)
        elif command == "exit":
            break
        else:
            print("Unrecognized command. Type 'help' to see the list of available commands.")


if __name__ == "__main__":
    user_interface()
