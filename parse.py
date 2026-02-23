import os

from pathlib import Path
from lib.helper import load_json
from excel.character_helper import (
    get_character_by_id,
    get_released_character_list
)
from character_story.character_scenario import parsing_character_story
from character_story.character_messanger import parsing_character_messanger
from character_story.character_valentine import parsing_character_valentine

if __name__ == '__main__':
    excels_path = os.path.join(os.getcwd(), "Excels")
    character_path = os.path.join(excels_path, "Character.json")
    scenario_path = os.path.join(excels_path, "ScenarioScript.json")
    messanger_path = os.path.join(excels_path, "AcademyMessanger.json")
    valentine_path = os.path.join(excels_path, "EventContentMeetup.json")
    
    character_data = load_json(character_path)
    scenario_data = load_json(scenario_path)
    messanger_data = load_json(messanger_path)
    valentine_data = load_json(valentine_path)
    
    character_list = get_released_character_list(character_data)
    
    # Parsing character momotalk story from scenario & messanger
    for character_scenario in character_list:
        character_output_dir = Path(os.getcwd(), "CharacterScenario", f"{character_scenario['Id']}_{character_scenario['DevName']}")
        parsing_character_story(scenario_data, character_scenario["Id"], character_output_dir)
    for character_messanger in character_list:
        character_output_txt = Path(os.getcwd(), "CharacterMessanger", f"{character_messanger['Id']}_{character_messanger['DevName']}.txt")
        parsing_character_messanger(messanger_data, character_messanger["Id"], character_output_txt)
        
    # Parsing character valentine story
    for valentine_character in valentine_data:
        valentine_char_data = get_character_by_id(character_data, valentine_character["CharacterId"])
        character_valentine_txt = Path(os.getcwd(), "CharacterValentine", f"{valentine_char_data['Id']}_{valentine_char_data['DevName']}.txt")
        parsing_character_valentine(scenario_data, valentine_character["ConditionScenarioGroupId"], valentine_character["CharacterId"], character_valentine_txt)
    