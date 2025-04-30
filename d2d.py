import requests
import os
import json

# Load config
TOKEN = os.environ.get("MTIwODM2OTQ2MDUyNDg3NTg0OQ.GJs0Mf.3mkv_2afQ32_ZtXrQ2o8UhegvXZMpdTL8DEAGU")
FROM_CHANNEL = os.environ.get("1211260758474883084")
TO_CHANNEL = os.environ.get("1211267595618222170")

HEADERS = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

LAST_ID_FILE = "last_id.txt"

def get_last_msg_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_msg_id(msg_id):
    with open(LAST_ID_FILE, "w") as f:
        f.write(msg_id)

def fetch_new_messages(after_id=None):
    params = {"limit": 10}
    if after_id:
        params["after"] = after_id
    r = requests.get(
        f"https://discord.com/api/v9/channels/{FROM_CHANNEL}/messages",
        headers=HEADERS,
        params=params
    )
    r.raise_for_status()
    return r.json()

def forward_message(msg):
    username = msg['author']['username']
    content = msg.get('content', '')
    msg_data = f"🤖 {username}\n{content}"

    # Send message
    requests.post(
        f"https://discord.com/api/v9/channels/{TO_CHANNEL}/messages",
        headers=HEADERS,
        json={"content": msg_data}
    )

def main():
    last_id = get_last_msg_id()
    messages = fetch_new_messages(after_id=last_id)

    if messages:
        messages = sorted(messages, key=lambda m: int(m["id"]))  # old to new
        for msg in messages:
            forward_message(msg)
            save_last_msg_id(msg['id'])

if __name__ == "__main__":
    main()
