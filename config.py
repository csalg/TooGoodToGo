# Intervals
SERVER_QUERY_INTERVAL = 300 # Interval between server queries
WAIT_AFTER_ERROR_INTERVAL = 30*60 # Time to wait before retrying if there is an error.
ITEM_RELISTED_INTERVAL = 2*60*60 # Assume an item was relisted if last time seen was more than interval

# E-Mail details
SERVER = "mail.cock.li"
PORT = 465  # For SSL
SENDER_EMAIL = "notifier-email@cock.li"
RECEIVER_EMAILS = ["someone@gmail.com", "someone-else@gmail.com"]
PASSWORD = "changeme"

# TooGoodToGo endpoints and payload
# Use a MITM like HttpCanary to capture the request from the app
URL = "https://apptoogoodtogo.com/api/item/v6/"
HEADERS = {
    "Authorization": "Bearer XXXXXXXXXXXXXXXXXXXX",
    'Content-Type': 'application/json'
}
DATA = {
    "user_id": "XXXXXX",
    "origin": {
        "latitude": 55.7375207,
        "longitude": 12.44979
    },
    "radius": 5.0,
    "page_size": 400,
    "page": 1,
    "discover": False,
    "favorites_only": False,
    "item_categories": [],
    "diet_categories": [],
    "with_stock_only": True,
    "hidden_only": False,
    "we_care_only": False
}

