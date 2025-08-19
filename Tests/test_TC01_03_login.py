"""Login test cases covering data-driven login, URL accessibility, and UI validation."""

import pytest
from utilities.logger import log_test

class TestLogin:
    def test_data_driven_login(self, driver, login_page, test_data):
        """Test Case 1: Data-driven login testing using CSV data"""
        try:
            # Extract credentials from test data fixture
            credentials = test_data.get("credentials", [])
            assert len(credentials) > 0, "No credentials loaded from CSV"
            
            # Loop through each credential set from CSV
            for credential in credentials:
                # Navigate to fresh login page for each test
                login_page.navigate_to_login_page()
                login_page.login(credential['username'], credential['password'])
                
                # Handle valid credentials - should reach dashboard
                if credential['expected_result'] == 'valid':
                    from pages.dashboard_page import DashboardPage
                    dashboard_page = DashboardPage(driver)
                    # Clean logout to prepare for next iteration
                    dashboard_page.logout()
                else:
                    # Handle invalid credentials - should stay on login or show error
                    current_url = login_page.get_current_url()
                    assert ("login" in current_url.lower() or 
                           login_page.is_error_message_displayed()), "Invalid credentials should show error or stay on login page"
            
            log_test("test_data_driven_login", "PASSED")
        except Exception as e:
            log_test("test_data_driven_login", "FAILED")
            raise
    
    def test_home_url_accessibility(self, driver, login_page):
        """Test Case 2: Verify that the home URL is accessible"""
        try:
            # Navigate to the base URL and verify it loads correctly
            login_page.navigate_to_login_page()
            # Simple heuristic check that we reached the OrangeHRM site
            assert "orangehrm" in login_page.get_current_url().lower()
            log_test("test_home_url_accessibility", "PASSED")
        except Exception as e:
            log_test("test_home_url_accessibility", "FAILED")
            raise
    
    def test_login_page_elements(self, driver, login_page):
        """Test Case 3: Validate presence of login fields"""
        try:
            # Load the login page first
            login_page.navigate_to_login_page()
            
            # Check username field exists and is functional
            assert login_page.is_element_visible(login_page.USERNAME_FIELD), "Username field is not visible"
            username_element = driver.find_element(*login_page.USERNAME_FIELD)
            assert username_element.is_enabled(), "Username field is not enabled"
            
            # Check password field exists and is functional
            assert login_page.is_element_visible(login_page.PASSWORD_FIELD), "Password field is not visible"
            password_element = driver.find_element(*login_page.PASSWORD_FIELD)
            assert password_element.is_enabled(), "Password field is not enabled"
            
            # Check login button exists and is functional
            assert login_page.is_element_visible(login_page.LOGIN_BUTTON), "Login button is not visible"
            login_button_element = driver.find_element(*login_page.LOGIN_BUTTON)
            assert login_button_element.is_enabled(), "Login button is not enabled"
            
            log_test("test_login_page_elements", "PASSED")
            
        except Exception as e:
            log_test("test_login_page_elements", "FAILED")
            raise
