from pathlib import Path
from typing import Dict, List, Any

from lib.helper import save_toml
from lib.character_name import extract_character_name, resolve_character_name


def parsing_event_story(event_data, scenario_groups: Dict[int, list], output_root: Path, character_name_map: dict):
    written_files = 0
    written_lines = 0

    for event_record in event_data:
        event_content_id = event_record.get("EventContentId")
        order = event_record.get("Order")
        for group_id in event_record.get("ScenarioGroupId") or []:
            script_rows: List[Dict[str, Any]] = scenario_groups.get(group_id)
            if not script_rows:
                continue

            translations: Dict[str, str] = {}
            line_counter = 0
            for record in script_rows:
                text_jp = str(record.get("TextJp", ""))
                if not text_jp.strip():
                    continue
                line_counter += 1
                key = f"{group_id}-{line_counter}"
                speaker_kr = extract_character_name(record.get("ScriptKr", ""))
                if speaker_kr:
                    key += f"-{resolve_character_name(character_name_map, speaker_kr)}"
                translations[key] = text_jp

            if not translations:
                continue

            output_file = Path(output_root, str(event_content_id), f"{group_id}_{order}.toml")
            save_toml(str(output_file), translations)
            written_files += 1
            written_lines += len(translations)

    print(f"Event story: wrote {written_files} files, {written_lines} lines.")
