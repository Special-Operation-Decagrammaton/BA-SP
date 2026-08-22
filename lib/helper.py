import os
import json

from collections import defaultdict


def load_json(json_path: str):
    try:
        with open(json_path, "r", encoding="utf-8") as infile:
            raw_data = json.load(infile)
        if isinstance(raw_data, dict) and "DataList" in raw_data:
            raw_data = raw_data["DataList"]
        return raw_data
    except FileNotFoundError as e:
        print(f"Error: Input JSON file not found at {json_path}")
        raise e
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from {json_path}")
        raise e

def save_json(json_path: str, data: dict):
    try:
        directory = os.path.dirname(json_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(json_path, "w", encoding="utf-8") as outfile:
            json.dump(data, outfile, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error: Could not save JSON to {json_path}")
        raise e

def group_records(records, key: str) -> dict:
    grouped = defaultdict(list)
    for record in records:
        value = record.get(key)
        if value is not None:
            grouped[value].append(record)
    return dict(grouped)

def save_toml(toml_path: str, translations: dict):
    try:
        directory = os.path.dirname(toml_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        lines = ["[translation]"]
        for key, value in translations.items():
            lines.append(f"{json.dumps(str(key), ensure_ascii=False)} = {json.dumps(str(value), ensure_ascii=False)}")
        with open(toml_path, "w", encoding="utf-8", newline="\n") as outfile:
            outfile.write("\n".join(lines) + "\n")
    except Exception as e:
        print(f"Error: Could not save TOML to {toml_path}")
        raise e