from bisect import bisect_right
from pathlib import Path
from typing import Dict, List, Any

from lib.helper import save_toml
from lib.character_name import extract_character_name, resolve_character_name

SCOPED_MODE_TYPES = ("Main", "Prologue", "SpecialOperation", "Sub", "Mini")
UNREFERENCED_GAP_LIMIT = 50


def build_translations(script_rows: List[Dict[str, Any]], group_id: int, character_name_map: dict) -> Dict[str, str]:
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
    return translations


def parsing_main_story(mode_data, scenario_groups: Dict[int, list], output_root: Path, character_name_map: dict):
    referenced_owners: Dict[int, List[Dict[str, Any]]] = {}
    for mode_record in mode_data:
        if mode_record.get("ModeType") not in SCOPED_MODE_TYPES:
            continue
        for group_id in mode_record.get("FrontScenarioGroupId") or []:
            referenced_owners.setdefault(group_id, []).append(mode_record)

    def output_file_for(mode_record: Dict[str, Any], group_id: int) -> Path:
        return Path(
            output_root,
            str(mode_record["ModeType"]),
            str(mode_record["SubType"]),
            f"Vol{str(mode_record["VolumeId"])}",
            f"Chap{str(mode_record["ChapterId"])}",
            f"{group_id}_Ep{mode_record['EpisodeId']}.toml",
        )

    written_files = 0
    written_lines = 0

    def write_translations(mode_record: Dict[str, Any], group_id: int, translations: Dict[str, str]):
        nonlocal written_files, written_lines
        save_toml(str(output_file_for(mode_record, group_id)), translations)
        written_files += 1
        written_lines += len(translations)

    for group_id, owners in referenced_owners.items():
        if group_id not in scenario_groups:
            continue
        translations = build_translations(scenario_groups[group_id], group_id, character_name_map)
        for mode_record in owners:
            write_translations(mode_record, group_id, translations)

    sorted_referenced = sorted(referenced_owners)
    for group_id in sorted(scenario_groups):
        if group_id in referenced_owners:
            continue
        index = bisect_right(sorted_referenced, group_id) - 1
        if index < 0:
            continue
        nearest = sorted_referenced[index]
        if group_id - nearest > UNREFERENCED_GAP_LIMIT:
            continue
        translations = build_translations(scenario_groups[group_id], group_id, character_name_map)
        for mode_record in referenced_owners[nearest]:
            write_translations(mode_record, group_id, translations)

    print(f"Main story: wrote {written_files} files, {written_lines} lines.")
