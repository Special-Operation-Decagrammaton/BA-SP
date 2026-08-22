import xxhash

from lib.helper import load_json


def load_character_name_map(json_path):
    rows = load_json(json_path)
    return {row["CharacterName"]: row.get("NameJP", "") for row in rows}


def extract_character_name(line: str):
    if not line or not line.strip():
        return None
    script_line = str(line).split("\n", 1)[0]
    parts = script_line.split(";")
    command = parts[0].strip().lower()

    if command == "#na" or command == "#q":
        if len(parts) == 3:
            return parts[1].strip()
    elif not command.startswith("#") and not command.startswith("["):
        if len(parts) >= 2:
            return parts[1].strip()

    return None


def resolve_character_name(character_name_map: dict, kr_name):
    if not kr_name:
        return None
    hash_key = xxhash.xxh32(str(kr_name).encode("utf-8")).intdigest()
    jp_name = character_name_map.get(hash_key)
    return jp_name if jp_name else kr_name
