import json
import os

MAPPING_FILE = os.path.join(os.path.dirname(__file__), "user_mapping.json")

def save_username_mapping(user_id: int, username: str):
    data = {}
    if os.path.exists(MAPPING_FILE):
        try:
            with open(MAPPING_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass
    
    data[str(user_id)] = username
    
    try:
        with open(MAPPING_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        import sys
        print(f"[user_mapping] Error saving user mapping: {e}", file=sys.stderr)
        sys.stderr.flush()

def get_username_from_id(user_id: int) -> str:
    if os.path.exists(MAPPING_FILE):
        try:
            with open(MAPPING_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(str(user_id))
        except Exception:
            pass
    return None
