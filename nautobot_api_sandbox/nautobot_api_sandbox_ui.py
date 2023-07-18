from .nauto_demo_functions import DemoNautobotClient


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


from .nauto_demo_functions import DemoNautobotClient

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
    api_token = input("Please enter your api token: ")
    nautobot_client = DemoNautobotClient(api_token=api_token)
    print(welcome_msg)

    # Commands that need an argument
    commands_with_arg = ["show_devices", "create_tenant", "delete_tenant", "get_tenant_id"]

    while True:
        command_input = input("Enter a command: ").split(" ", 1)
        command = command_input[0]

        # Check if the command needs an argument and if it was provided
        if command in commands_with_arg:
            if len(command_input) == 1:
                print(f"The {command} command requires an argument.")
                continue
            else:
                arg = command_input[1].strip()

        if command == "show_sites":
            nautobot_client.show_sites()
        elif command == "show_devices":
            nautobot_client.show_devices(arg)
        elif command == "create_tenant":
            nautobot_client.create_tenant(arg)
        elif command == "delete_tenant":
            nautobot_client.delete_tenant(arg)
        elif command == "show_tenants":
            nautobot_client.show_tenants()
        elif command == "get_tenant_id":
            nautobot_client.get_tenant_id(arg)
        elif command == "help":
            print(welcome_msg)
        elif command == "exit":
            break
        else:
            print("Unrecognized command. Type 'help' to see the list of available commands.")