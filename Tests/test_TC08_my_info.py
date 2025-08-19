"""My Info test cases verifying submenu presence and navigation."""

import pytest
from utilities.logger import log_test

class TestMyInfo:
    def test_my_info_menu_items(self, logged_in_session):
        """Test Case 8: Validate the presence of menu items under "My Info" """
        try:
            # Use logged-in session to access dashboard
            driver, login_page, dashboard_page = logged_in_session
            
            # Navigate to My Info section
            dashboard_page.click_my_info_menu()
            
            # Verify that My Info sub-menu items are present and clickable
            # Expected sub-menu items: Personal Details, Contact Details, Emergency Contacts, etc.
            assert dashboard_page.verify_my_info_submenu_items()
            
            log_test("test_my_info_menu_items", "PASSED")
        except Exception as e:
            log_test("test_my_info_menu_items", "FAILED")
            raise 
