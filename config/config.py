"""Configuration settings for OrangeHRM automation test suite.

This module contains all configuration constants including:
- Base URL and default credentials for the demo site
- Timeout values for implicit and explicit waits
- Directory paths for reports and logs
- Automatic directory creation for output folders

The configuration is designed to work with the OrangeHRM demo at:
https://opensource-demo.orangehrmlive.com
"""

from pathlib import Path

# Base application settings
BASE_URL = "https://opensource-demo.orangehrmlive.com"  # Demo OrangeHRM instance
VALID_USERNAME = "Admin"  # Default admin username for demo
VALID_PASSWORD = "admin123"  # Default admin password for demo

# WebDriver timeout configurations
IMPLICIT_WAIT = 10  # Global implicit wait in seconds
EXPLICIT_WAIT = 20  # Default explicit wait timeout in seconds

# Project directory structure
PROJECT_ROOT = Path(__file__).parent.parent  # Root directory of the project
REPORTS_DIR = PROJECT_ROOT / "reports"  # HTML test reports location
LOGS_DIR = PROJECT_ROOT / "logs"  # Automation execution logs

# Ensure output directories exist before test execution
for directory in [REPORTS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)  # Create directories if they don't exist
