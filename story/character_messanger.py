from pathlib import Path
from typing import List, Dict, Any

from lib.helper import save_toml

def parsing_character_messanger(messanger_data, target_character_id: int, text_output_path: Path):
    filtered_records: List[Dict[str, Any]] = []

    for record in messanger_data:
        if record.get("CharacterId") == target_character_id:
            filtered_records.append(record)

    if not filtered_records:
        print(f"No records found for CharacterId: {target_character_id}")
        return

    sorted_records = sorted(
        filtered_records,
        key=lambda r: r.get("MessageGroupId", 0)
    )

    translations: Dict[str, str] = {}
    for record in sorted_records:
        messager_id = record.get("Id", "N/A")
        msg_jp = record.get("MessageJP", "").strip()

        translations[f"{messager_id}"] = msg_jp

    try:
        save_toml(str(text_output_path), translations)
        # print(f"✅ Successfully wrote {len(sorted_records)} messages for CharacterId {target_character_id} to {text_output_path.name}")
    except IOError:
        print(f"Error: Could not write output file: {text_output_path}")
