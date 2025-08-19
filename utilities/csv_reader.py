"""CSV reader utilities for data-driven testing.

- Reads login credentials from CSV, creating a sample file if missing
- Provides a small helper to log a quick summary for visibility
"""

import csv
from pathlib import Path


def read_credentials():
    """Read credentials from CSV file, creating a sample if not present.

    Returns:
        list[dict]: Each row contains username, password, expected_result, description
    """
    csv_file = Path(__file__).parent.parent / "test_data" / "test_credentials.csv"
    
    # Create test_data directory if it doesn't exist
    csv_file.parent.mkdir(exist_ok=True)
    
    if not csv_file.exists():
        # Create sample CSV file with a few representative rows
        sample_data = [
            {'username': 'Admin', 'password': 'admin123', 'expected_result': 'valid', 'description': 'Valid admin'},
            {'username': 'InvalidUser', 'password': 'InvalidPass', 'expected_result': 'invalid', 'description': 'Invalid user'},
            {'username': '', 'password': '', 'expected_result': 'invalid', 'description': 'Empty credentials'}
        ]
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['username', 'password', 'expected_result', 'description'])
            writer.writeheader()
            writer.writerows(sample_data)
    
    credentials = []
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Normalize empty values (explicitly keep as empty strings)
            if row['username'] == '':
                row['username'] = ''
            if row['password'] == '':
                row['password'] = ''
            credentials.append(row)
    
    return credentials


def log_credentials_summary(credentials):
    """Print a short summary of how many credentials were loaded.

    Args:
        credentials (list[dict]): List of credential dictionaries
    """
    valid_count = sum(1 for c in credentials if c.get('expected_result') == 'valid')
    print(f"Loaded {len(credentials)} credentials ({valid_count} valid)")
