"""Claim page object to submit expense claims via OrangeHRM.

Provides helpers to select claim event and currency, enter remarks, and
submit the form with basic success verification.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ClaimPage(BasePage):
    # Locators
    EVENT_DROPDOWN = (By.XPATH, "//label[text()='Event']/ancestor::div[contains(@class,'oxd-input-group')]//div[@class='oxd-select-text oxd-select-text--active']")
    CURRENCY_DROPDOWN = (By.XPATH, "//label[text()='Currency']/ancestor::div[contains(@class,'oxd-input-group')]//div[@class='oxd-select-text oxd-select-text--active']")
    REMARKS_TEXTAREA = (By.XPATH, "//label[text()='Remarks']/ancestor::div[contains(@class,'oxd-input-group')]//textarea")
    SUBMIT_BUTTON = (By.XPATH, "//button[@type='submit']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[@class='oxd-toast-content oxd-toast-content--success']")

    def is_claim_page_loaded(self):
        """Check if Submit Claim page header is visible."""
        try:
            self.wait_for_element_visible((By.XPATH, "//h6[contains(text(),'Submit Claim')]"))
            return True
        except:
            return False

    # Selects the Event Type
    def select_event(self, event_type="Travel"):
        """Select an event type (first available option)."""
        try:
            self.wait_for_element_clickable(self.EVENT_DROPDOWN)
            self.click_element(self.EVENT_DROPDOWN)
            options = self.driver.find_elements(By.XPATH, "//div[@class='oxd-select-option']//span")
            if options:
                options[0].click()
                return True
            return False
        except Exception:
            return False
    
    # Selects the Currency
    def select_currency(self, currency="USD"):
        """Select a currency (first available option)."""
        try:
            self.wait_for_element_clickable(self.CURRENCY_DROPDOWN)
            self.click_element(self.CURRENCY_DROPDOWN)
            options = self.driver.find_elements(By.XPATH, "//div[@class='oxd-select-option']//span")
            if options:
                options[0].click()
                return True
            return False
        except Exception:
            return False
    
    # Fills the Remarks Section
    def enter_remarks(self, remarks="Business travel expenses"):
        """Type remarks into the claim form."""
        try:
            self.wait_for_element_visible(self.REMARKS_TEXTAREA)
            self.enter_text(self.REMARKS_TEXTAREA, remarks)
            return True
        except Exception:
            return False

    def submit_claim(self):
        """Click submit button."""
        try:
            self.wait_for_element_clickable(self.SUBMIT_BUTTON)
            self.click_element(self.SUBMIT_BUTTON)
            return True
        except Exception:
            return False

    def is_success_message_displayed(self):
        """Return True if success toast appears."""
        try:
            self.wait_for_element_visible(self.SUCCESS_MESSAGE)
            return True
        except:
            return False

    def fill_claim_form(self, event_type="Travel", currency="USD", remarks="Business travel expenses"):
        """Fill form fields and submit the claim."""
        try:
            self.select_event(event_type)
            self.select_currency(currency)
            self.enter_remarks(remarks)
            return self.submit_claim()
        except Exception:
            return False
