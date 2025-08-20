import pytest
import random
import string
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.logger import log_test
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
import time


class TestClaimManagement:

    def test_initiate_claim_request(self, driver, claim_page):
        """
        Test Case 10: Initiate a Claim Request
        Steps:
        1. Login as Admin
        2. Create a new ESS Employee user
        3. Logout as Admin
        4. Login as new ESS Employee
        5. Navigate to Claim section
        6. Initiate and submit a new claim
        7. Verify the claim appears in My Claims
        """
        try:
            wait = WebDriverWait(driver, 15)

            # --- Step 1: Login as Admin ---
            login_page = LoginPage(driver)
            dashboard_page = DashboardPage(driver)
            login_page.navigate_to_login_page()
            login_page.login("Admin", "admin123")   # 🔹 OrangeHRM demo admin creds
            assert dashboard_page.is_dashboard_loaded(), "Admin login failed"

            # --- Step 2: Create a new ESS Employee user ---
            rand_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
            new_username = f"testuser{rand_str}"
            new_password = "TestUser123"
            employee_name = "Thomas Kutty Benny"  # Existing employee in demo DB

            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Admin']"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Add']"))).click()

            # Select User Role = ESS
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[text()='-- Select --'])[1]"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='ESS']"))).click()

            # Assign Employee
            emp_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Type for hints...']")))
            emp_input.send_keys(employee_name)
            wait.until(EC.element_to_be_clickable((By.XPATH, f"//span[text()='{employee_name}']"))).click()

            # Status = Enabled
            wait.until(EC.element_to_be_clickable((By.XPATH, "(//div[@class='oxd-select-text--after'])[2]"))).click()
            wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Enabled']"))).click()

            # Username + Password
            user_fields = driver.find_elements(By.XPATH, "(//label[text()='Username']/following::input)")
            user_fields[0].send_keys(new_username)
            user_fields[1].send_keys(new_password)
            user_fields[2].send_keys(new_password)

            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()=' Save ']"))).click()
            wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'oxd-toast')][contains(.,'Success')]")))

            # --- Step 3: Logout as Admin ---
            dashboard_page.logout()

            # --- Step 4: Login as new ESS Employee ---
            login_page.navigate_to_login_page()
            login_page.login(new_username, new_password)
            assert dashboard_page.is_dashboard_loaded(), "ESS Employee login failed"

            # --- Step 5: Navigate to Claim section ---
            driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/claim/submitClaim")
            wait.until(EC.any_of(
                EC.presence_of_element_located((By.XPATH, "//h6[contains(text(),'Submit Claim')]")),
                EC.presence_of_element_located((By.XPATH, "//label[contains(text(),'Event')]")),
                EC.presence_of_element_located((By.XPATH, "//button[@type='submit']"))
            ))

            # --- Step 6: Initiate and submit a new claim ---
            event_name = "Travel Allowance"
            remarks = "Business travel expenses"

            claim_filled = claim_page.fill_claim_form(
                event_type=event_name,
                currency="Afghanistan Afghani",
                remarks=remarks
            )
            assert claim_filled, "Failed to fill claim form"
            assert claim_page.is_success_message_displayed(), "No success message after submission"

            #  Verify the claim appears in My Claims ---
        
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


            # Verify in table
            rows = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@role='table']//div[@role='row']")))
            assert any(event_name in row.text and remarks in row.text for row in rows), \
                   f"{event_name} claim with remarks '{remarks}' not found in My Claims"

            log_test("test_initiate_claim_request", "PASSED")

        except Exception as e:
            log_test("test_initiate_claim_request", f"FAILED - {str(e)}")
            raise

        print("✅ Test Case 10 executed successfully") 
        time.sleep(5)
