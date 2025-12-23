def get_released_character_list(character_data):
    released_characters = []
    for character in character_data:
        if character["IsPlayable"] == True and character["IsPlayableCharacter"] == True and character["IsDummy"] == False and character["IsNPC"] == False and character["ProductionStep"] == "Release" and character["CombatStyleIndex"] == 0:
            released_characters.append(character)
    return released_characters