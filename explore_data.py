import json
from pathlib import Path

# Project root
ROOT = Path(__file__).resolve().parent.parent

# Load tickets
with open(ROOT / "data" / "tickets.json", "r", encoding="utf-8") as f:
    tickets = json.load(f)

# Load accounts
with open(ROOT / "data" / "accounts.json", "r", encoding="utf-8") as f:
    accounts = json.load(f)

print("=" * 60)
print("DATASET SUMMARY")
print("=" * 60)

print(f"\nTotal Tickets : {len(tickets)}")
print(f"Total Accounts: {len(accounts)}")

print("\nFirst Ticket:\n")
print(json.dumps(tickets[0], indent=4))

print("\nFirst Account:\n")
print(json.dumps(accounts[0], indent=4))