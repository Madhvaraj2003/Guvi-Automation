"""Single-run script to add a user via OrangeHRM demo and exit.

This is a minimal version using raw Selenium calls with brief sleeps.
Prefer the Page Object Model tests for scalable automation.
"""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# Launch Chrome and log in as Admin
driver = webdriver.Chrome()
driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')
driver.maximize_window()
driver.implicitly_wait(20)
driver.find_element(By.NAME, value="username").send_keys("Admin")
driver.find_element(By.NAME, value="password").send_keys("admin123")
driver.find_element(By.XPATH, value="//button[text()=' Login ']").click()

# Navigate to add user and fill mandatory fields
driver.find_element(By.XPATH, value="//span[text()='Admin']").click()
driver.find_element(By.XPATH, value="//button[text()=' Add ']").click()
driver.find_element(By.XPATH, value="(//div[text()='-- Select --'])[1]").click()
driver.find_element(By.XPATH, value="//span[text()='ESS']").click()
driver.find_element(By.XPATH, value="//input[@placeholder='Type for hints...']").send_keys("Thomas Kutty Benny")
driver.find_element(By.XPATH, value="//span[text()='Thomas Kutty Benny']").click()

# Sleep to allow UI updates; for production use, replace with explicit waits
time.sleep(10)

# Status and credentials
driver.find_element(By.XPATH, value="(//div[@class='oxd-select-text--after'])[2]").click()
driver.find_element(By.XPATH, value="//span[text()='Enabled']").click()
driver.find_element(By.XPATH, value="(//label[text()='Username']/following::input)[1]").send_keys("demotestuser1454")
driver.find_element(By.XPATH, value="(//label[text()='Username']/following::input)[2]").send_keys("demotestuser12378")
driver.find_element(By.XPATH, value="(//label[text()='Username']/following::input)[3]").send_keys("demotestuser12378")
driver.find_element(By.XPATH, value="//button[text()=' Save ']").click()

# Non-interactive end: briefly wait to observe result, then quit
time.sleep(5)
driver.quit()




# //button[@class='oxd-button oxd-button--medium oxd-button--secondary orangehrm-button-margin'









