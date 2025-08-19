"""Project-wide logger configuration and helper.

Configures a simple file-based logger that writes into logs/automation.log.
A small helper `log_test` is exposed to record test-level pass/fail notes.
"""

import logging
from config.config import LOGS_DIR

# Create a module-level logger
logger = logging.getLogger('orangehrm')
logger.setLevel(logging.INFO)

# File handler with a simple time + message format
handler = logging.FileHandler(LOGS_DIR / "automation.log")
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(handler)


def log_test(test_name, status):
    """Write a succinct test result line to the log file.

    Args:
        test_name (str): Name of the test function
        status (str): Status or note (e.g., PASSED/FAILED or more details)
    """
    logger.info(f"{test_name}: {status}")
