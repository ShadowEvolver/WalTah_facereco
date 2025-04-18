import os
import json

DB_PATH = "registered_users/user_db.json"
if not os.path.exists(DB_PATH):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, 'w') as f:
        json.dump({}, f)

def register_user(name, label, image_path):
    with open(DB_PATH, 'r+') as f:
        db = json.load(f)
        db[str(label)] = {"name": name, "image": image_path}
        f.seek(0); f.truncate()
        json.dump(db, f, indent=2)


def get_user_info(label):
    with open(DB_PATH, 'r') as f:
        db = json.load(f)
    return db.get(str(label), {"name": "Unknown", "image": None})
