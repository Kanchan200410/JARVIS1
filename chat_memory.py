import json
import os

FILE = "chat_history.json"

def load_chat():
    if not os.path.exists(FILE):
        return []
    with open(FILE, "r") as f:
        return json.load(f)

def save_chat(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_chat(role, message):
    data = load_chat()
    data.append({"role": role, "content": message})
    save_chat(data)

def get_chat():
    return load_chat()