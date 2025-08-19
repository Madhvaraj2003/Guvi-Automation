"""Simple entry point to run the Pytest suite.

This script invokes `pytest` in a subprocess so the test suite can be
launched via `python runner_tests.py`. All pytest configuration lives in
pytest.ini and the Tests/ directory.
"""

import subprocess


def run_tests():
    """Invoke pytest with default settings configured in pytest.ini."""
    subprocess.run(["pytest"])  # Inherit current working directory and env


if __name__ == "__main__":
    run_tests()
