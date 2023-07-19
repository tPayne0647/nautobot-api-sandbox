Nautobot API Sandbox
This is a simple program to test my programming knowledge and learn more about API and Nautobot.

Prerequisites
Before getting started, make sure you have the following installed on your machine:

* Python 3.9 or later
* Poetry

Getting Started
1.) Clone the rerepository: git clone git@github.com:tPayne0647/nautobot-api-sandbox.git
2.) Navigate to the project directory: cd nautobot-api-sandbox
3.) Install the project dependencies using Poetry: poetry install
4.) Activate the virtual environment created by Poetry: poetry shell
5.) Run the program: python nautobot_api_sandbox/nautobot_api_sandbox_ui.py

Demo token: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

This will start the Nautobot API Sandbox command-line interface.
Follow the instructions in the application to interact with the Nautobot API.
NOTE- you don't need to add '()' or "". just simply type the command + the name (eg. create_tenant tpayne, show_devices atl01)


Development
If you're contributing to the project or want to run tests, make sure to install the development dependencies as well: poetry install --dev
To run the tests: poetry run pytest
any help or tips would be awesome!




-currently working on/ want to add
* exception handling? Need to learn more about how these work exactly... 
* valid unittest?
* integrate click?
* make sure using logging correctly
* poetry integration

This is a work in progress!!!
