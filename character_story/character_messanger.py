from pathlib import Path
from typing import List, Dict, Any

def parsing_character_messanger(messanger_data, target_character_id: int, text_output_txt: Path):
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
    
    output_lines = []
    for record in sorted_records:
        character_id = record.get("CharacterId", "N/A")
        messager_id = record.get("Id", "N/A")
        msg_kr = record.get("MessageKR", "").strip()
        msg_jp = record.get("MessageJP", "").strip()

        output_block = (
            f"{character_id} | {messager_id}\n"
            f"MessageKR: {msg_kr}\n"
            f"MessageJP: {msg_jp}\n"
        )
        output_lines.append(output_block)
        
    final_output_content = "\n".join(output_lines)
    
    try:
        text_output_txt.parent.mkdir(parents=True, exist_ok=True)
        with open(text_output_txt, "w", encoding="utf-8") as outfile:
            outfile.write(final_output_content)
        
        # print(f"✅ Successfully wrote {len(sorted_records)} messages for CharacterId {target_character_id} to {text_output_txt.name}")
    except IOError:
        print(f"Error: Could not write output file: {text_output_txt}")