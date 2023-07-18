from class_refactor import DemoNautobotClient

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
    while True:
        command = input("Enter a command: ")
        if command == "show_sites":
            nautobot_client.show_sites()
        elif command.startswith("help"):
            print(welcome_msg)
        elif command == "exit":
            break
        
user_interface()