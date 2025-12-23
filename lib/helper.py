import json
from pathlib import Path

def load_json(json_path: Path):
    try:
        with open(json_path, "r", encoding="utf-8") as infile:
            raw_data = json.load(infile)
        return raw_data
    except FileNotFoundError as e:
        print(f"Error: Input JSON file not found at {json_path}")
        raise e
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from {json_path}")
        raise e

def save_json(json_path: Path, data: dict):
    try:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error: Could not save JSON to {json_path}")
        raise e