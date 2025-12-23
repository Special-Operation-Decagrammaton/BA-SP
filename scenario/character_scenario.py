from pathlib import Path
from collections import defaultdict
from typing import List, Dict

def parsing_character_story(scenario_data, character_id: int, text_output_dir: Path):
    grouped_output_lines: Dict[int, List[str]] = defaultdict(list)
    line_counters_per_group: Dict[int, int] = defaultdict(int)
    
    for record in scenario_data:
        group_id = record.get("GroupId")
        text_jp = record.get("TextJp", "")

        if group_id is None:
            continue
        
        first_char_group = int(f"{character_id}00")
        last_char_group = int(f"{character_id}99")
        if first_char_group <= group_id <= last_char_group:
            line_counters_per_group[group_id] += 1
            line_number = line_counters_per_group[group_id]

            safe_text = str(text_jp).replace('\\', '\\\\').replace('\r\n', '\\n').replace('\n', '\\n')
            formatted_line = f"{group_id}-{line_number:04d}: {safe_text}"
            grouped_output_lines[group_id].append(formatted_line)

    if not grouped_output_lines:
        print("No valid entries found in the GroupId range.")
        return

    text_output_dir.mkdir(parents=True, exist_ok=True)

    total_lines = 0
    for group_id, lines in grouped_output_lines.items():
        output_file = text_output_dir / f"{character_id}_{group_id}.txt"
        try:
            with open(output_file, "w", encoding="utf-8") as outfile:
                outfile.write("\n".join(lines) + "\n")
            total_lines += len(lines)
        except IOError:
            print(f"Error: Could not write file for GroupId {group_id}: {output_file}")

    print(f"✅ Successfully writing for character {character_id}, {len(grouped_output_lines)} files, {total_lines} total lines.")
