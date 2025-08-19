"""Ad-hoc script to create a user in OrangeHRM demo using raw Selenium calls.

Note: This script is for manual demonstration only. Prefer using the
Page Object Model and pytest tests in the Tests/ directory for
maintainable automation.
"""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize a Chrome browser (requires chromedriver via PATH or manager)
driver = webdriver.Chrome()

# Open login page and log in as Admin
driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
driver.maximize_window()
driver.implicitly_wait(20)
driver.find_element(By.NAME, value="username").send_keys("Admin")
driver.find_element(By.NAME, value="password").send_keys("admin123")
driver.find_element(By.XPATH, value="//button[text()=' Login ']").click()

# Navigate to Admin -> Add User
driver.find_element(By.XPATH, value="//span[text()='Admin']").click()
driver.find_element(By.XPATH, value="//button[text()=' Add ']").click()

# User Role: ESS
driver.find_element(By.XPATH, value="(//div[text()='-- Select --'])[1]").click()
driver.find_element(By.XPATH, value="//span[text()='ESS']").click()

# Select Employee Name suggestion
driver.find_element(By.XPATH, value="//input[@placeholder='Type for hints...']").send_keys("Thomas Kutty Benny")
driver.find_element(By.XPATH, value="//span[text()='Thomas Kutty Benny']").click()

# Wait for UI to settle (demo-only; consider explicit waits instead)
time.sleep(10)

# Status: Enabled
driver.find_element(By.XPATH, value="(//div[@class='oxd-select-text--after'])[2]").click()
driver.find_element(By.XPATH, value="//span[text()='Enabled']").click()

# Credentials
driver.find_element(By.XPATH, value="(//label[text()='Username']/following::input)[1]").send_keys("demotestuser1")
driver.find_element(By.XPATH, value="(//label[text()='Username']/following::input)[2]").send_keys("demotestuser123")
driver.find_element(By.XPATH, value="(//label[text()='Username']/following::input)[3]").send_keys("demotestuser123")

# Save
driver.find_element(By.XPATH, value="//button[text()=' Save ']").click()

# Keep browser open until Enter is pressed (for manual inspection)
input("Press enter to exit..")

