import os

from pathlib import Path
from lib.helper import load_json, group_records
from lib.character_name import load_character_name_map
from lib.character_helper import (
    get_character_by_id,
    get_released_character_list
)
from story.character_scenario import parsing_character_story
from story.character_messanger import parsing_character_messanger
from story.character_valentine import parsing_character_valentine
from story.main_story import parsing_main_story
from story.event_story import parsing_event_story

if __name__ == '__main__':
    excels_path = os.path.join(os.getcwd(), "Excels")
    character_path = os.path.join(excels_path, "CharacterExcelTable.json")
    scenario_paths = [
        os.path.join(excels_path, "ScenarioScriptExcelTable1.json"),
        os.path.join(excels_path, "ScenarioScriptExcelTable2.json"),
    ]
    messanger_path = os.path.join(excels_path, "AcademyMessangerExcelTable.json")
    valentine_path = os.path.join(excels_path, "EventContentMeetupExcelTable.json")
    scenario_mode_path = os.path.join(excels_path, "ScenarioModeExcelTable.json")
    event_scenario_path = os.path.join(excels_path, "EventContentScenarioExcelTable.json")
    character_name_path = os.path.join(excels_path, "ScenarioCharacterNameExcelTable.json")
    
    character_data = load_json(character_path)
    scenario_data = []
    for scenario_path in scenario_paths:
        scenario_data.extend(load_json(scenario_path))
    messanger_data = load_json(messanger_path)
    valentine_data = load_json(valentine_path)
    scenario_mode_data = load_json(scenario_mode_path)
    event_scenario_data = load_json(event_scenario_path)
    character_name_map = load_character_name_map(character_name_path)
    
    character_list = get_released_character_list(character_data)
    scenario_groups = group_records(scenario_data, "GroupId")
    messanger_groups = group_records(messanger_data, "CharacterId")
    
    # Parsing character momotalk story from scenario & messanger
    for character_scenario in character_list:
        character_output_dir = Path(os.getcwd(), "CharacterScenario", f"{character_scenario['Id']}_{character_scenario['DevName']}")
        parsing_character_story(scenario_groups, character_scenario["Id"], character_output_dir, character_name_map)
    for character_messanger in character_list:
        character_output_toml = Path(os.getcwd(), "CharacterMessanger", f"{character_messanger['Id']}_{character_messanger['DevName']}.toml")
        parsing_character_messanger(messanger_groups.get(character_messanger["Id"], []), character_messanger["Id"], character_output_toml)
        
    # Parsing character valentine story
    for valentine_character in valentine_data:
        valentine_char_data = get_character_by_id(character_data, valentine_character["CharacterId"])
        character_valentine_toml = Path(os.getcwd(), "CharacterValentine", f"{valentine_char_data['Id']}_{valentine_char_data['DevName']}.toml")
        parsing_character_valentine(scenario_groups.get(valentine_character["ConditionScenarioGroupId"], []), valentine_character["ConditionScenarioGroupId"], valentine_character["CharacterId"], character_valentine_toml, character_name_map)
        
    # Parsing main story
    main_story_output_dir = Path(os.getcwd(), "MainStory")
    parsing_main_story(scenario_mode_data, scenario_groups, main_story_output_dir, character_name_map)

    # Parsing event story
    event_story_output_dir = Path(os.getcwd(), "EventStory")
    parsing_event_story(event_scenario_data, scenario_groups, event_story_output_dir, character_name_map)
    