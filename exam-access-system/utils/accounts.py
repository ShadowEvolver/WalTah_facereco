import os
import json

ACCOUNTS_PATH = "accounts/accounts.json"
if not os.path.exists(ACCOUNTS_PATH):
    os.makedirs(os.path.dirname(ACCOUNTS_PATH), exist_ok=True)
    with open(ACCOUNTS_PATH, 'w') as f:
        # Example default: {"exam1": "password123"}
        json.dump({"exam1": "password123"}, f, indent=2)

def authenticate(username, password):
    """Returns True if credentials match."""
    with open(ACCOUNTS_PATH, 'r') as f:
        accounts = json.load(f)
    return accounts.get(username) == password