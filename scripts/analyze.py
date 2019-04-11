#!/usr/bin/env python3

import json
import os

from jinja2 import Environment, FileSystemLoader

base_dir = "/".join(os.path.realpath(__file__).split("/")[:-2]) # yes, this is janky. no, I don't care
data_dir = os.path.join(base_dir, "data")
results_file = os.path.join(base_dir, "results.md")
env = Environment(loader=FileSystemLoader(os.path.join(base_dir, "jinja_templates")))

with open(os.path.join(data_dir, 'info.json'),'r') as f:
    info = json.load(f)

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

for season in info:
    sinfo = info[season]
    characters = []
    for char in sinfo:
        character = sinfo[char]
        character['Name'] = char
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
    print("Season {}:".format(int(season)-1))
    for i in range(len(characters)):
        c = characters[i]
        print("{}: {} ({})".format(i+1, c["Name"], c["Total"]))

print("\n\n\n")
character_averages = []
for cname in character_map:
    char = character_map[cname]
    char["Average"] = round(float(char["Total"])/float(len(char["Seasons"])),1)
    character_averages.append((cname, char["Average"], char["Total"], len(char["Seasons"])))
    # print("{} : {} ({} in {})".format(cname, float(char["Total"])/float(len(char["Seasons"])), char["Total"], len(char["Seasons"])))
character_averages.sort(key = lambda c: c[1], reverse=True)
for char in character_averages:
    print("{} : {}\n>>>>({} total points in {} point-earning seasons)".format(*char))

# place = 1
# with open(results_file, "w") as f:
#     f.write("## Character points:\n")
#     for char in character_averages:
#         by_season = 
#         f.write('''
#         ### {place}: {0} : {1}
# {2} total points in {3} point-earning seasons'''.strip().format(*char, place=place))
#         f.write('\n')
#         place += 1
place = 1


character_bundles = []

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
        "place":place
    }
    for season in char["Seasons"][::-1]:
        season_blob = {
            "number":int(season)-1,
            "total":char[season]["Total"],
            "categories":{k:char[season][k] for k in char[season] if char[season][k] and k not in ['ID','Total','Name']}
        }
    
    place += 1
    character_bundles.append(character_bundle)

template_name = "results.md"
with open(results_file,"w") as f:
    f.write(env.get_template(template_name).render(characters=character_bundles))

# with open(results_file, "w") as f:
#     f.write("## Character points:\n")
#     for chardata in character_averages:
#         char_name = chardata[0]
#         avg_points = chardata[1]
#         total_points = chardata[2]
#         season_count = chardata[3]
#         char = character_map[char_name]
#         f.write('''
#         ### {place}: {char_name} : {avg_points}
# <details><summary>{total_points} total points in {season_count} point-earning seasons</summary><p>'''.strip().format(char_name=char_name, avg_points=avg_points, total_points=total_points, season_count=season_count, place=place))
#         f.write('\n')
#         for season in char["Seasons"]:
#             points = char[season]["Total"]
#             f.write('#### Season {season}: {points}\n'.format(season=int(season)-1, points=points))
#         f.write('</p></details>\n')
#         place += 1
#     # char = character_map[cname]
#     # char["Average"] = round(float(char["Total"])/float(len(char["Seasons"])),1)
#     # character_averages.append((cname, char["Average"], char["Total"], len(char["Seasons"])))
