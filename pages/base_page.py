"""Base Page Object implementing common WebDriver operations.

This module provides the foundation for all page objects in the test suite,
containing reusable methods for element interaction with explicit waits.
All page objects inherit from this class to maintain consistency.

Key Features:
- Centralized WebDriver wait management
- Common element interaction methods
- Timeout handling with fallbacks
- Standardized error handling patterns
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.config import EXPLICIT_WAIT

class BasePage:
    """Base class for all page objects containing common WebDriver operations.
    
    This class provides standardized methods for interacting with web elements
    using explicit waits to ensure reliable test execution.
    """
    
    def __init__(self, driver):
        """Initialize the base page with WebDriver instance.
        
        Args:
            driver: WebDriver instance for browser automation
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)  # Default wait instance

    def _get_wait(self, timeout=None):
        """Get WebDriverWait instance with specified or default timeout.
        
        Args:
            timeout: Custom timeout in seconds, uses default if None
            
        Returns:
            WebDriverWait instance with appropriate timeout
        """
        return WebDriverWait(self.driver, timeout) if timeout else self.wait

    def find_element(self, locator, timeout=None):
        """Find element with explicit wait"""
        return self._get_wait(timeout).until(EC.presence_of_element_located(locator))

    def click_element(self, locator, timeout=None):
        """Click element with explicit wait"""
        self._get_wait(timeout).until(EC.element_to_be_clickable(locator)).click()

    def enter_text(self, locator, text, timeout=None):
        """Enter text in element with explicit wait"""
        element = self.find_element(locator, timeout)
        element.clear()
        element.send_keys(text)

    def clear_and_type(self, locator, text, timeout=None):
        """Clear input and type text (alias for enter_text)"""
        self.enter_text(locator, text, timeout)

    def is_element_visible(self, locator, timeout=None):
        """Check if element is visible with explicit wait"""
        try:
            self._get_wait(timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def wait_for_element_visible(self, locator, timeout=None):
        """Wait for element to be visible"""
        self._get_wait(timeout).until(EC.visibility_of_element_located(locator))

    def wait_for_element_clickable(self, locator, timeout=None):
        """Wait for element to be clickable"""
        self._get_wait(timeout).until(EC.element_to_be_clickable(locator))

    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url

    def get_page_title(self):
        """Get page title"""
        return self.driver.title