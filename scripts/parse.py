#!/usr/bin/env python3

import json
import os
import requests

RUN_SUFFIX=''

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

data_dir = os.path.join(os.path.realpath(__file__), "..", "data")

def download_page(season, character):
    url = 'http://fantasora.com/game/1/season/{season}/char/{character}'.format(season=season, character=character)
    output = requests.get(url).text
    lines = [l.strip() for l in output.split('\n')]
    char_name = None
    sort_lines = []
    for line in lines:
        line = line.strip()
        if 'Fatal error' in line:
            break
        if not char_name and 'data-scorer-thing-name' in line:
            char_name = line[24:-1].strip()
        elif char_name and 'data-sort-value' in line and len(sort_lines) < 8:
            sort_lines.append(line)
        if len(sort_lines) == 8:
            break
    score = {}
    total = 0
    if not char_name:
        return None, None
    for i in range(8):
        line = sort_lines[i]
        cat = keys[i]
        num = int(line[40:-2])
        score[cat] = num
        total += num
    score['Total'] = total
    score['ID'] = character
    return char_name, score

seasons = [8,2,3,4,5,6,7]
characters = 70

seasons_map = {}

for season in seasons:
    season_map = {}
    print("Season: {}".format(season-1))
    # for character in range(1,70):
    for character in range(1,300):
        name, score = download_page(season, character)
        if name:
            print("{}: {}".format(name, score['Total']))
            season_map[name] = score
        else:
            print("Char# {} undefined".format(character))
    with open(os.path.join(data_dir, 'season_{}.json{}'.format(season-1,RUN_SUFFIX)), 'w') as f:
        json.dump(season_map, f, indent=2, sort_keys=True)
    seasons_map[season] = season_map
with open(os.path.join(data_dir, 'info.json{}'.format(RUN_SUFFIX)),'w') as f:
    json.dump(seasons_map, f, indent=2, sort_keys=True)
