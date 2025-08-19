Automated Testing of OrangeHRM Demo

Overview
This repository contains an automated UI test suite for `https://opensource-demo.orangehrmlive.com`, covering login, navigation, user management, leave, claim, and forgot password flows using Selenium, Pytest, and the Page Object Model.

Project Structure
- `Tests/`: Pytest test cases and fixtures
- `pages/`: Page Objects encapsulating UI actions and locators
- `utilities/`: Driver factory, CSV reader, and logger
- `config/`: Config constants and directories
- `reports/`: HTML report output (generated)
- `logs/automation.log`: Execution logs

Setup
1) Python 3.10+
2) Install dependencies:
   pip install -r requirements.txt

Running Tests
- Default (Chrome):
  pytest -v -s

- Cross-browser:
  pytest -v -s --browser=firefox
  pytest -v -s --browser=edge

- HTML report is generated at `reports/report.html` (configured in `pytest.ini`).

Data-driven Login
- Credentials are read from `Test_data/test_credentials.csv`. If missing, a sample is generated automatically.

Key Test Cases
- TC1: Data-driven login (valid and invalid)
- TC2: Home URL accessibility
- TC3: Login fields presence
- TC4: All main menu items visible and clickable
- TC5: Create user and validate login
- TC6: Validate user appears in Admin list
- TC7: Forgot Password flow
- TC8: “My Info” submenu presence and navigation
- TC9: Assign leave and verify listing (best-effort on demo site)
- TC10: Submit claim and verify listing (best-effort on demo site)

Notes and Limitations
- The public demo may intermittently change UI/permissions. Tests include best-effort verification of listings for Leave/Claim and will fall back to success toast/URL checks when listings are unavailable.
- Explicit waits are used throughout; browser closes after each test via fixtures.

Logs and Reports
- Execution logs: `logs/automation.log`
- HTML report: `reports/report.html`

Contributing
- Follow POM structure, add explicit waits, and keep locators resilient.


