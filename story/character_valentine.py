from pathlib import Path
from typing import Dict

from lib.helper import save_toml
from lib.character_name import extract_character_name, resolve_character_name

def parsing_character_valentine(scenario_data, scenario_id: int, character_id: int, text_output_path: Path, character_name_map: dict) -> None:
    translations: Dict[str, str] = {}
    line_counter = 0

    for record in scenario_data:
        group_id = record.get("GroupId")
        text_jp = record.get("TextJp", "")

        if group_id == scenario_id:
            if not str(text_jp).strip():
                continue
            line_counter += 1
            key: str = f"{group_id}-{line_counter}"
            speaker_kr = extract_character_name(record.get("ScriptKr", ""))
            if speaker_kr:
                key += f"-{resolve_character_name(character_name_map, speaker_kr)}"
            translations[key] = str(text_jp)

    if not translations:
        print("No valid entries found in the GroupId range.")
        return

    try:
        save_toml(str(text_output_path), translations)
        # print(f"✅ Successfully writing for character valentine {character_id}, {len(translations)} total lines.")
    except IOError:
        print(f"Error: Could not write file for GroupId {scenario_id}: {text_output_path}")
