import pytest
from unittest.mock import MagicMock, patch
from nautobot_api_sandbox.nautobot_api_sandbox_ui import user_interface, WELCOME_MSG
from nautobot_api_sandbox.nauto_demo_functions import (
    DemoNautobotClient,
    TenantNotFoundError,
    SiteNotFoundError,
)


def test_show_sites_command():
    # Mock the input function to simulate user input
    with patch("builtins.input", side_effect=["api_token", "show_sites", "exit"]):
        # Mock the DemoNautobotClient class and its display_sites method
        mock_client = MagicMock()
        mock_client.display_sites.return_value = ["Site1", "Site2"]

        # Mock the DemoNautobotClient constructor to return the mock_client
        with patch(
            "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
            return_value=mock_client,
        ):
            user_interface()

        # Assert that display_sites was called once
        mock_client.display_sites.assert_called_once()


def test_show_devices_command():
    # Mock the input function to simulate user input
    with patch("builtins.input", side_effect=["api_token", "show_devices Test Site", "exit"]):
        # Mock the DemoNautobotClient class and its display_devices method
        mock_client = MagicMock()
        mock_client.display_devices.return_value = ["Device1", "Device2"]

        # Mock the DemoNautobotClient constructor to return the mock_client
        with patch(
            "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
            return_value=mock_client,
        ):
            user_interface()

        # Assert that display_devices was called once with "Site1" as an argument
        mock_client.display_devices.assert_called_once_with("Test Site")


def test_show_devices_invalid_site():
    # Mock the input function to simulate user input
    with patch("builtins.input", side_effect=["api_token", "show_devices Invalid Site", "exit"]):
        # Mock the DemoNautobotClient class and its display_devices method
        mock_client = MagicMock()
        mock_client.display_devices.side_effect = SiteNotFoundError("InvalidSite")

        # Mock the logger to capture log messages
        with patch("nautobot_api_sandbox.nautobot_api_sandbox_ui.logging.getLogger") as mock_logger:
            logger_instance = MagicMock()
            mock_logger.return_value = logger_instance

            # Mock the DemoNautobotClient constructor to return the mock_client
            with patch(
                "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
                return_value=mock_client,
            ):
                user_interface()

        # Assert that the logger.error method was called with the correct message
        logger_instance.error.assert_called_with(
            "Site %s not found. Please enter a valid site name.", "Invalid Site"
        )


def test_create_tenant_command():
    # Mock the input function to simulate user input
    with patch("builtins.input", side_effect=["api_token", "create_tenant Test Tenant", "exit"]):
        # Mock the DemoNautobotClient class and its create_tenant method
        mock_client = MagicMock()
        mock_client.create_tenant.return_value = ["Tenant Test Tenant created successfully."]

        # Mock the DemoNautobotClient constructor to return the mock_client
        with patch(
            "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
            return_value=mock_client,
        ):
            user_interface()

        # Assert that create_tenant was called once with "Test Tenant" as an argument
        mock_client.create_tenant.assert_called_once_with("Test Tenant")


def test_create_tenant_existing_command():
    # Mock the input function to simulate user input
    with patch(
        "builtins.input", side_effect=["api_token", "create_tenant Existing Tenant", "exit"]
    ):
        # Mock the DemoNautobotClient class and its create_tenant method
        mock_client = MagicMock()
        mock_client.create_tenant.return_value = None

        # Mock the logger to capture log messages
        with patch("nautobot_api_sandbox.nautobot_api_sandbox_ui.logging.getLogger") as mock_logger:
            logger_instance = MagicMock()
            mock_logger.return_value = logger_instance

            # Mock the DemoNautobotClient constructor to return the mock_client
            with patch(
                "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
                return_value=mock_client,
            ):
                user_interface()

        # Assert that the logger.error method was called with the correct message
        logger_instance.error.assert_called_with(
            "A tenant with the name '%s' already exists.", "Existing Tenant"
        )


def test_delete_tenant_command():
    # Mock the input function to simulate user input
    with patch("builtins.input", side_effect=["api_token", "delete_tenant Test Tenant", "exit"]):
        # Mock the DemoNautobotClient class and its delete_tenant method
        mock_client = MagicMock()
        mock_client.delete_tenant.return_value = (True, "Tenant deleted successfully.")

        # Mock the DemoNautobotClient constructor to return the mock_client
        with patch(
            "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
            return_value=mock_client,
        ):
            user_interface()

        # Assert that delete_tenant was called once with "Test Tenant" as an argument
        mock_client.delete_tenant.assert_called_once_with("Test Tenant")


def test_delete_nonexistent_tenant_command():
    # Mock the input function to simulate user input
    with patch(
        "builtins.input", side_effect=["api_token", "delete_tenant Nonexistent Tenant", "exit"]
    ):
        # Mock the DemoNautobotClient class and its delete_tenant method
        mock_client = MagicMock()
        mock_client.delete_tenant.side_effect = TenantNotFoundError("Nonexistent Tenant")

        # Mock the logger to capture log messages
        with patch("nautobot_api_sandbox.nautobot_api_sandbox_ui.logging.getLogger") as mock_logger:
            logger_instance = MagicMock()
            mock_logger.return_value = logger_instance

            # Mock the DemoNautobotClient constructor to return the mock_client
            with patch(
                "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
                return_value=mock_client,
            ):
                user_interface()

        # Assert that the logger.error method was called with the correct message
        logger_instance.error.assert_called_with(
            "Tenant with name '%s' not found.", "Nonexistent Tenant"
        )


def test_get_tenant_command():
    # Mock the input function to simulate user input
    with patch("builtins.input", side_effect=["api_token", "get_tenant Test Tenant", "exit"]):
        # Mock the DemoNautobotClient class and its display_tenant method
        mock_client = MagicMock()
        mock_client.display_tenant.return_value = "Tenant Test Tenant retrieved successfully."

        # Mock the DemoNautobotClient constructor to return the mock_client
        with patch(
            "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
            return_value=mock_client,
        ):
            user_interface()

        # Assert that display_tenant was called once with "Test Tenant" as an argument
        mock_client.display_tenant.assert_called_once_with("Test Tenant")


def test_get_nonexistent_tenant_command():
    # Mock the input function to simulate user input
    with patch(
        "builtins.input", side_effect=["api_token", "get_tenant Nonexistent Tenant", "exit"]
    ):
        # Mock the DemoNautobotClient class and its display_tenant method
        mock_client = MagicMock()
        mock_client.display_tenant.side_effect = TenantNotFoundError("Nonexistent Tenant")

        # Mock the logger to capture log messages
        with patch("nautobot_api_sandbox.nautobot_api_sandbox_ui.logging.getLogger") as mock_logger:
            logger_instance = MagicMock()
            mock_logger.return_value = logger_instance

            # Mock the DemoNautobotClient constructor to return the mock_client
            with patch(
                "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
                return_value=mock_client,
            ):
                user_interface()

        # Assert that the logger.error method was called with the correct message
        logger_instance.error.assert_called_with(
            "Tenant '%s' not found. Please enter a valid tenant name.", "Nonexistent Tenant"
        )


def test_show_tenants_command():
    # Mock the input function to simulate user input
    with patch("builtins.input", side_effect=["api_token", "show_tenants", "exit"]):
        # Mock the DemoNautobotClient class and its display_tenants method
        mock_client = MagicMock()
        mock_client.display_tenants.return_value = ["Tenant1", "Tenant2"]

        # Mock the DemoNautobotClient constructor to return the mock_client
        with patch(
            "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
            return_value=mock_client,
        ):
            user_interface()

        # Assert that display_tenants was called once
        mock_client.display_tenants.assert_called_once()


def test_help_command():
    # Mock the input function to simulate user input
    with patch("builtins.input", side_effect=["api_token", "help", "exit"]):
        # Mock the logger to capture log messages
        with patch("nautobot_api_sandbox.nautobot_api_sandbox_ui.logging.getLogger") as mock_logger:
            logger_instance = MagicMock()
            mock_logger.return_value = logger_instance

            # Mock the DemoNautobotClient constructor to return a mock_client
            with patch(
                "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
                return_value=MagicMock(),
            ):
                user_interface()

        # Assert that the logger.info method was called with the correct message
        logger_instance.info.assert_called_with(WELCOME_MSG)


def test_exit_command():
    # Mock the input function to simulate user input
    with patch("builtins.input", side_effect=["api_token", "exit"]):
        # Mock the DemoNautobotClient constructor to return a mock_client
        with patch(
            "nautobot_api_sandbox.nautobot_api_sandbox_ui.DemoNautobotClient",
            return_value=MagicMock(),
        ):
            user_interface()
    # If the function completes without error, this means the exit command worked.
    assert True
