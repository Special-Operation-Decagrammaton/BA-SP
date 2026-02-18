def get_released_character_list(character_data):
    released_characters = []
    for character in character_data:
        if character["IsPlayable"] == True and character["IsPlayableCharacter"] == True and character["IsDummy"] == False and character["IsNPC"] == False and character["ProductionStep"] == 3 and character["CombatStyleIndex"] == 0:
            released_characters.append(character)
    return released_characters

def get_character_by_id(character_data, character_id):
    for character in character_data:
        if character["Id"] == character_id:
            return character
    return None