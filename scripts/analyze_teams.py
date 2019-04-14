#!/usr/bin/env python3

import json
import os

from jinja2 import Environment, FileSystemLoader

base_dir = "/".join(os.path.realpath(__file__).split("/")[:-2]) # yes, this is janky. no, I don't care
data_dir = os.path.join(base_dir, "data")
results_file = os.path.join(base_dir, "results_teams.md")
env = Environment(loader=FileSystemLoader(os.path.join(base_dir, "jinja_templates")))

with open(os.path.join(data_dir, 'info_dragons.json'),'r') as f:
    info = json.load(f)
with open(os.path.join(data_dir, 'teams.json'),'r') as f:
    teams = json.load(f)

keys = [
    'Kills',
    'Insults',
    'Intercourse',
    'Wine',
    'Kills Cmd.',
    'Politics',
    'Deaths',
    'Special',
]
character_map = {}
character_ids = {}
for season in info:
    sinfo = info[season]
    characters = []
    for char in sinfo:
        character = sinfo[char]
        character['Name'] = char
        if char not in character_ids:
            character_ids[char] = character["ID"]
        characters.append(character)
        allchar = character_map.get(char, {})
        if character["Total"] > 0:
            acseasons = allchar.get("Seasons",[])
            acseasons.append(season)
            allchar["Seasons"] = acseasons
            allchar[season] = sinfo[char]
            for key in keys + ["Total"]:
                allchar[key] = sinfo[char][key] + allchar.get(key, 0)
            character_map[char] = allchar
    characters.sort(key = lambda c: c["Total"], reverse=True)

character_averages = []
for cname in character_map:
    char = character_map[cname]
    char["Average"] = round(float(char["Total"])/float(len(char["Seasons"])),1)
    character_averages.append((cname, char["Average"], char["Total"], len(char["Seasons"])))
character_averages.sort(key = lambda c: c[1], reverse=True)
place = 1

character_bundles = []

character_names_by_id = { character_ids[k]:k for k in character_ids}

characters_by_id = {}

for chardata in character_averages:
    char_name = chardata[0]
    avg_points = chardata[1]
    total_points = chardata[2]
    season_count = chardata[3]
    char = character_map[char_name]
    character_bundle = {
        "name":char_name,
        "avg_points":avg_points,
        "total_points":total_points,
        "season_count":season_count,
        "seasons":[],
        "place":place,
        "id": character_ids[char_name],
        "link": "https://fantasora.com/char/{id}".format(id=character_ids[char_name])
    }
    for season in char["Seasons"][::-1]:
        season_blob = {
            "link":"https://fantasora.com/game/1/season/{season}/char/{id}".format(season=season, id=character_ids[char_name]),
            "number":int(season)-1,
            "total":char[season]["Total"],
            "categories":{k:char[season][k] for k in char[season] if char[season][k] and k not in ['ID','Total','Name']}
        }
        character_bundle["seasons"].append(season_blob)

    place += 1
    character_bundles.append(character_bundle)
    characters_by_id[character_ids[char_name]] = character_bundle
    
print(json.dumps(characters_by_id, indent=2, sort_keys=True))

for team in teams:
    roster_ids = [int(x["ID"]) for x in team["Characters"] if int(x["ID"]) in characters_by_id]
    team_roster = [characters_by_id.get(x) for x in roster_ids if characters_by_id.get(x)]
    point_list = [c["avg_points"] for c in team_roster]
    expected_points = sum([c["avg_points"] for c in team_roster])
    team["ExpectedScore"] = expected_points
teams.sort(key=lambda x: x["ExpectedScore"])
print(json.dumps(teams, indent=2, sort_keys=True))



# template_name = "results.md"
# with open(results_file,"w") as f:
#     f.write(env.get_template(template_name).render(characters=character_bundles))
