"""WebDriver factory with cross-browser support.

Creates and returns a Selenium WebDriver instance for Chrome, Firefox, or
Edge using webdriver-manager to provision drivers automatically.

The browser can be selected via:
- Function parameter `browser`
- Environment variable `BROWSER`
- Default fallback: Chrome
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import IMPLICIT_WAIT
import os


def get_driver(browser: str | None = None):
    """Return a configured WebDriver instance for the requested browser.

    Args:
        browser: Optional browser name ('chrome'|'firefox'|'edge'). If None, use env var BROWSER or default to 'chrome'.

    Returns:
        selenium.webdriver: A ready-to-use WebDriver with implicit wait and maximized window.
    """
    browser_name = (browser or os.environ.get("BROWSER") or "chrome").lower()

    if browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    else:
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    # Apply common settings
    driver.implicitly_wait(IMPLICIT_WAIT)
    try:
        driver.maximize_window()  # May fail in some headless/CI environments
    except Exception:
        pass
    return driver
