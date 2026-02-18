from pathlib import Path
from collections import defaultdict
from typing import List, Dict

def parsing_character_valentine(scenario_data, scenario_id: int, character_id: int, text_output_path: Path) -> None:
    grouped_output_lines: Dict[int, List[str]] = defaultdict(list)
    line_counters_per_group: Dict[int, int] = defaultdict(int)
    
    for record in scenario_data:
        group_id = record.get("GroupId")
        text_jp = record.get("TextJp", "")
        
        if group_id == scenario_id:
            line_counters_per_group[group_id] += 1
            line_number = line_counters_per_group[group_id]

            safe_text = str(text_jp).replace('\\', '\\\\').replace('\r\n', '\\n').replace('\n', '\\n')
            formatted_line = f"{group_id}-{line_number:04d}: {safe_text}"
            grouped_output_lines[group_id].append(formatted_line)
            
    if not grouped_output_lines:
        print("No valid entries found in the GroupId range.")
        return

    text_output_path.parent.mkdir(parents=True, exist_ok=True)
    
    total_lines = 0
    for group_id, lines in grouped_output_lines.items():
        try:
            with open(text_output_path, "w", encoding="utf-8") as outfile:
                outfile.write("\n".join(lines) + "\n")
            total_lines += len(lines)
        except IOError:
            print(f"Error: Could not write file for GroupId {group_id}: {text_output_path}")

    # print(f"✅ Successfully writing for character valentine {character_id}, {total_lines} total lines.")