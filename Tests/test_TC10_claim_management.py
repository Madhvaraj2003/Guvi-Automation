import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.logger import log_test
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
import time
class TestClaimManagement:

    def test_initiate_claim_request(self, driver, claim_page):
        """Test Case 10: Employee initiates a claim request and verifies in claim history"""
        try:
            wait = WebDriverWait(driver, 15)

            # --- Employee login ---
            login_page = LoginPage(driver)
            dashboard_page = DashboardPage(driver)
            login_page.navigate_to_login_page()
            login_page.login("employee", "employee123")   # 🔹 use your ESS creds
            assert dashboard_page.is_dashboard_loaded(), "Employee login failed"

            # --- Submit Claim ---
            driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/claim/submitClaim")

            wait.until(EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//h6[contains(text(),'Submit Claim')]")),
                EC.presence_of_element_located((By.XPATH, "//label[contains(text(),'Event')]")),
                EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
            ))

            event_name = "Accommodation"
            remarks = "Automated Claim Test"

            claim_filled = claim_page.fill_claim_form(
                event_type=event_name,
                currency="Indian Rupee",
                remarks=remarks
            )
            assert claim_filled, "Failed to fill claim form"
            assert claim_page.is_success_message_displayed(), "No success message shown after submission"

            # --- Go to My Claims ---
            my_claims_menu = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'My Claims')]")))
            my_claims_menu.click()

            # --- Filter by Event Name ---
            event_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='oxd-select-text-input']")))
            event_dropdown.click()

            option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{event_name}']")))
            option.click()

            # Click Search button
            search_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
            search_btn.click()

            # --- Verify record in table ---
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='table']")))
            rows = driver.find_elements(By.XPATH, "//div[@role='table']//div[@role='row']")
            assert len(rows) > 1, f"No {event_name} claims found in history"

            # Optional: verify remarks text also appears in table
            table_text = driver.find_element(By.XPATH, "//div[@role='table']").text
            assert remarks in table_text, "Submitted claim not found in history table"

            log_test("test_initiate_claim_request", "PASSED")

        except Exception as e:
            log_test("test_initiate_claim_request", f"FAILED - {str(e)}")
            raise
        
        print("testcase executed successfully")
        time.sleep(5)