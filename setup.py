from setuptools import setup, find_packages

setup(
    name="nautobot_api_sandbox",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pynautobot"],
    entry_points={
        "console_scripts": [
            "nautobot_api_sandbox=nautobot_api_sandbox.nautobot_api_sandbox_ui:user_interface",
        ],
    },
)
