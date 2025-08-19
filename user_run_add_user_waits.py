"""Script to add a user with robust explicit waits and retry helpers.

This example demonstrates a more resilient approach compared to raw
sleep-based scripts by using WebDriverWait and small utility functions.
"""

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_click(driver, xpath, timeout=20):
    """Wait until an element is clickable and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )


def wait_visible(driver, xpath, timeout=20):
    """Wait until an element is visible and return it."""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath))
    )


def try_click_first_present(driver, xpaths, timeout_each=6):
    """Try clicking the first clickable element among xpaths; return True if clicked."""
    for xp in xpaths:
        try:
            elem = WebDriverWait(driver, timeout_each).until(
                EC.element_to_be_clickable((By.XPATH, xp))
            )
            elem.click()
            return True
        except Exception:
            continue
    return False


def main():
    """Create a user using the Admin UI, then attempt to log in with it."""
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

        # Login as Admin
        wait_visible(driver, "//input[@name='username']").send_keys("Admin")
        wait_visible(driver, "//input[@name='password']").send_keys("admin123")
        wait_click(driver, "//button[normalize-space()='Login']").click()

        # Wait for dashboard (flexible heuristics)
        WebDriverWait(driver, 30).until(
            EC.any_of(
                EC.url_contains("/dashboard"),
                EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']")),
                EC.visibility_of_element_located((By.XPATH, "//span[normalize-space()='Admin']")),
            )
        )

        # Go to Admin → Add User
        wait_click(driver, "//span[normalize-space()='Admin']").click()
        wait_click(driver, "//button[normalize-space()='Add']").click()

        # User Role = ESS
        wait_click(driver, "(//label[normalize-space()='User Role']/following::div[contains(@class,'oxd-select-text')])[1]").click()
        try_click_first_present(
            driver,
            [
                "//div[@role='listbox']//span[normalize-space()='ESS']",
                "//span[normalize-space()='ESS']",
            ],
        )

        # Employee Name = pick an existing one
        emp_input = wait_visible(driver, "//label[normalize-space()='Employee Name']/following::input[@placeholder='Type for hints...']")
        emp_input.clear()
        emp_input.send_keys("Paul")

        # Choose suggestion (prefer Paul Collings, else first option)
        clicked_emp = try_click_first_present(
            driver,
            [
                "//div[@role='listbox']//span[normalize-space()='Paul Collings']",
                "(//div[@role='listbox']//div[contains(@class,'oxd-autocomplete-option')])[1]",
                "(//div[contains(@class,'oxd-autocomplete-option')])[1]",
            ],
        )
        if not clicked_emp:
            raise RuntimeError("Could not select an employee suggestion")

        # Status = Enabled
        wait_click(driver, "(//label[normalize-space()='Status']/following::div[contains(@class,'oxd-select-text')])[1]").click()
        try_click_first_present(
            driver,
            [
                "//div[@role='listbox']//span[normalize-space()='Enabled']",
                "//span[normalize-space()='Enabled']",
            ],
        )

        # Create unique username/password
        suffix = datetime.now().strftime("%H%M%S")
        new_username = f"demouser{suffix}"
        new_password = f"DemoUser@{suffix}"

        # Username
        wait_visible(driver, "//label[normalize-space()='Username']/ancestor::div[contains(@class,'oxd-input-group')]//input").send_keys(new_username)
        # Password
        wait_visible(driver, "//label[normalize-space()='Password']/ancestor::div[contains(@class,'oxd-input-group')]//input").send_keys(new_password)
        # Confirm Password
        wait_visible(driver, "//label[normalize-space()='Confirm Password']/ancestor::div[contains(@class,'oxd-input-group')]//input").send_keys(new_password)

        # Save
        wait_click(driver, "//button[normalize-space()='Save']").click()

        # Wait for success (either toast or return to list)
        WebDriverWait(driver, 20).until(
            EC.any_of(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'oxd-toast')][contains(.,'Success')]")),
                EC.url_contains("/viewSystemUsers"),
            )
        )

        # Logout
        wait_click(driver, "//span[@class='oxd-userdropdown-tab']").click()
        wait_click(driver, "//a[normalize-space()='Logout']").click()

        # Attempt login with new user
        wait_visible(driver, "//input[@name='username']").send_keys(new_username)
        wait_visible(driver, "//input[@name='password']").send_keys(new_password)
        wait_click(driver, "//button[normalize-space()='Login']").click()

        # Verify login result (demo may not persist users). Accept either dashboard or error.
        try:
            WebDriverWait(driver, 15).until(
                EC.any_of(
                    EC.visibility_of_element_located((By.XPATH, "//h6[text()='Dashboard']")),
                    EC.visibility_of_element_located((By.XPATH, "//p[contains(@class,'oxd-alert-content-text')]")),
                    EC.url_contains("/dashboard"),
                )
            )
        except Exception:
            pass

        # Print credentials for visibility in terminal
        print(f"Created username: {new_username}")
        print(f"Password: {new_password}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()














