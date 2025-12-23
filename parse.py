import os

from pathlib import Path
from lib.helper import load_json
from character.character_retrieval import get_released_character_list
from scenario.character_scenario import parsing_character_story
from messanger.character_messanger import parsing_character_messanger

if __name__ == '__main__':
    excels_path = Path(os.getcwd(), "Excels")
    character_path = Path(excels_path, "Character.json")
    scenario_path = Path(excels_path, "ScenarioScript.json")
    messanger_path = Path(excels_path, "AcademyMessanger.json")
    
    character_data = load_json(character_path)
    scenario_data = load_json(scenario_path)
    messanger_data = load_json(messanger_path)
    
    character_list = get_released_character_list(character_data)
    
    # Parsing character story from scenario
    for character in character_list:
        character_output_dir = Path(os.getcwd(), "CharacterScenario", f"{character['Id']}_{character['DevName']}")
        parsing_character_story(scenario_data, character["Id"], character_output_dir)
    
    # Parsing character story from messanger/momotalk
    for character in character_list:
        character_output_txt = Path(os.getcwd(), "CharacterMessanger", f"{character['Id']}_{character['DevName']}.txt")
        parsing_character_messanger(messanger_data, character["Id"], character_output_txt)
    