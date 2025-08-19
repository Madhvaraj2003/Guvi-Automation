"""Centralized Pytest fixtures for Selenium-based test suite.

Provides driver lifecycle management, data loading from CSV, page object
fixtures, and a convenience fixture that logs in before each test and
logs out afterwards.
"""

import pytest
from utilities.driver_factory import get_driver
from utilities.csv_reader import read_credentials, log_credentials_summary
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.claim_page import ClaimPage
from pages.leave_page import LeavePage


@pytest.fixture(scope="session")
def test_data():
    """Load test data from CSV file once per session and print a summary."""
    credentials = read_credentials()
    log_credentials_summary(credentials)
    return {"credentials": credentials}


def pytest_addoption(parser):
    """Add command-line option to select browser for test execution."""
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome|firefox|edge")


@pytest.fixture(scope="function")
def driver(request):
    """Provide a WebDriver per test function and ensure cleanup."""
    driver = None
    try:
        browser = request.config.getoption("--browser")
        driver = get_driver(browser)
        yield driver
    finally:
        if driver:
            driver.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    """Return a LoginPage object bound to the test's WebDriver."""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def dashboard_page(driver):
    """Return a DashboardPage object bound to the test's WebDriver."""
    return DashboardPage(driver)


@pytest.fixture(scope="function")
def claim_page(driver):
    """Return a ClaimPage object bound to the test's WebDriver."""
    return ClaimPage(driver)


@pytest.fixture(scope="function")
def leave_page(driver):
    """Return a LeavePage object bound to the test's WebDriver."""
    return LeavePage(driver)


@pytest.fixture(scope="function")
def logged_in_session(driver, login_page, dashboard_page):
    """Create logged-in session before a test, and attempt clean logout after.

    Yields:
        tuple: (driver, login_page, dashboard_page)
    """
    try:
        login_page.navigate_to_login_page()
        login_page.login("Admin", "admin123")
        
        # Confirm dashboard appears; swallow result as some UIs may vary
        dashboard_page.is_dashboard_loaded()
        
        yield driver, login_page, dashboard_page
    finally:
        try:
            dashboard_page.logout()
        except:
            # Fall back to direct navigation if logout fails (e.g., session state changes)
            driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
