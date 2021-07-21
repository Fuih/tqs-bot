from discord import Color

FACTIONS = {
    'Thục': 1,
    'Quần': 3,
    'Ngụy': 5,
    'Ngô': 7
}

FACTION_COLORS = {
    FACTIONS['Thục']: Color.red(),
    FACTIONS['Quần']: Color.dark_grey(),
    FACTIONS['Ngụy']: Color.blue(),
    FACTIONS['Ngô']: Color.green(),
    FACTIONS['Thục']*FACTIONS['Quần']: Color.dark_red(),
    FACTIONS['Thục']*FACTIONS['Ngụy']: Color.purple(),
    FACTIONS['Thục']*FACTIONS['Ngô']: Color.from_rgb(255, 255, 0),
    FACTIONS['Quần']*FACTIONS['Ngụy']: Color.from_rgb(102, 153, 204),
    FACTIONS['Quần']*FACTIONS['Ngô']: Color.teal(),
    FACTIONS['Ngụy']*FACTIONS['Ngô']: Color.from_rgb(0,255,255),
}

def get_faction_color(faction):
    faction = faction.split('/')
    if len(faction) > 1:
        return FACTION_COLORS[FACTIONS[faction]]

    faction_value = FACTIONS[faction[0]] * FACTIONS[faction[1]]
    return FACTION_COLORS[faction_value]