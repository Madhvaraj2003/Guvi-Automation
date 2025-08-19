"""Navigation test cases verifying main menu visibility post-login."""

import pytest
from utilities.logger import log_test

class TestNavigation:
    def test_main_menu_items_visibility(self, logged_in_session):
        """Test Case 4: Verify visibility of main menu items after login"""
        try:
            # Reuse the logged-in session (driver + page objects)
            driver, login_page, dashboard_page = logged_in_session

            # Expected top-level navigation items to be visible
            menu_items = [
                ("Admin", dashboard_page.ADMIN_MENU),
                ("PIM", dashboard_page.PIM_MENU),
                ("Leave", dashboard_page.LEAVE_MENU),
                ("Time", dashboard_page.TIME_MENU),
                ("Recruitment", dashboard_page.RECRUITMENT_MENU),
                ("My Info", dashboard_page.MY_INFO_MENU),
                ("Performance", dashboard_page.PERFORMANCE_MENU),
                ("Dashboard", dashboard_page.DASHBOARD_MENU),
            ]

            # Assert each menu item is present/visible in the DOM
            for menu_name, locator in menu_items:
                assert dashboard_page.is_element_visible(locator), f"Menu '{menu_name}' is not visible"

            log_test("test_main_menu_items_visibility", "PASSED")

        except Exception:
            log_test("test_main_menu_items_visibility", "FAILED")
            raise
