import os
from dotenv import load_dotenv
from retell import Retell

load_dotenv()
client = Retell(api_key=os.getenv("RETELL_API_KEY"))

# Note: The SDK 'create' method typically buys a number.
# We first need to see if there is a 'search' method or if 'create' just assigns one.
# Based on common patterns, 'create' might buy from a pool or creating a request.
# Let's try to list existing numbers first.

print("Listing existing phone numbers...")
try:
    numbers = client.phone_number.list()
    for num in numbers:
        print(f"Number: {num.phone_number} (ID: {num.phone_number_pretty})")
except Exception as e:
    print(f"Error listing numbers: {e}")

# IMPORTANT: Buying a number cost money. We should be careful.
# Usually API has a buy/create method.
# client.phone_number.create(phone_number_pretty="...") or similar.
