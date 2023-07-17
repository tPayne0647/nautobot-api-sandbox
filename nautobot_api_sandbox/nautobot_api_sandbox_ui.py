from .nauto_demo_functions import *

welcome_msg = """
                       Welcome to tPayne's nautobot demo API sandbox!
      ************************************************************************************
        Here is a list of available commands:
        show_sites.............................Get list of all sites
        show_devices [SITE NAME]...............Get count of devices and list device names
        create_tenant [TENANT NAME]............Create a new tenant with specified name
        get_tenant_id [TENANT NAME]............Get UUID of specified tenant
        delete_tenant [TENANT NAME]............Delete specified tenant
        show_tenants...........................Get count and list all tenant names
        help...................................Reprint this window
        
      ************************************************************************************
      """


def user_interface():
    print(welcome_msg)
    while True:
        command = input("Enter a command: ")
        if command == "show_sites":
            show_sites()
        elif command.startswith("show_devices"):
            _, site_name = command.split(" ", 1)
            show_devices(site_name.strip())
        elif command.startswith("create_tenant"):
            _, tenant_name = command.split(" ", 1)
            create_tenant(tenant_name.strip())
        elif command.startswith("delete_tenant"):
            _, tenant_name = command.split(" ", 1)
            delete_tenant(tenant_name.strip())
        elif command.startswith("show_tenants"):
            show_tenants()
        elif command.startswith("get_tenant_id"):
            _, name = command.split(" ", 1)
            get_tenant_id(name.strip())
        elif command.startswith("help"):
            print(welcome_msg)
        elif command == "exit":
            break