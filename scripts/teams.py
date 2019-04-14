#!/usr/bin/env python3
import json

with open('info.json.1','r') as f:
    info = json.load(f)

teams = {
    "The Imp's Delight":[81,23,27,3,270],
    "Win Or Die":[67,82,258,101,73],
    "Valar Morghulis":[5,40,36,37,126],
    "Stick them with the pointy end":[17,28,105,68,193],
    "I drink and I know things":[6,79,80,191,213],
    "Wights Sox":[18,50,72,84,263],
    "The North Dismembers":[39,59,63,190,195],
    "Always Paying Debts":[7,61,13,102,92],
    "GOT GOAT":[19,130,32,189,233],
    "Four-eyed Raven(claw)":[31,52,38,45,161],
    "oysters, clams, and cockles!":[9,216,91,221,219]
}





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
cid_map = {}
for season in info:
    sinfo = info[season]
    characters = []
    for char in sinfo:
        character = sinfo[char]
        schar = sinfo[char]
        char = char.strip()
        cid_map[str(character["ID"])] = char
        character['Name'] = char
        characters.append(character)
        allchar = character_map.get(char, {})
        if character["Total"] > 0:
            acseasons = allchar.get("Seasons",[])
            acseasons.append(season)
            allchar["Seasons"] = acseasons
            allchar["Name"] = char
            allchar[season] = schar
            allchar["ID"] = schar
            for key in keys + ["Total"]:
                allchar[key] = schar[key] + allchar.get(key, 0)
            character_map[char] = allchar
    characters.sort(key = lambda c: c["Total"], reverse=True)
    print("Season {}:".format(season))
    for i in range(len(characters)):
        c = characters[i]
        print("{}: {} ({})".format(i+1, c["Name"], c["Total"]))

print("\n\n\n")
character_averages = []
for cname in character_map:
    char = character_map[cname]
    char["Average"] = float(char["Total"])/float(len(char["Seasons"]))
    character_averages.append((cname, char["Average"], char["Total"], len(char["Seasons"])))
    # print("{} : {} ({} in {})".format(cname, float(char["Total"])/float(len(char["Seasons"])), char["Total"], len(char["Seasons"])))
character_averages.sort(key = lambda c: c[1], reverse=True)
cid_avg_map = {str(c):0 for c in cid_map}
for char in character_averages:
    print("{} : {} ({} in {})".format(*char))
    cid_avg_map[str(character_map[char[0]]["ID"])] = char[1]

print(json.dumps(cid_map, indent=2, sort_keys=True))
print(json.dumps(cid_avg_map, indent=2, sort_keys=True))

#full_teams = 
for tname in teams:
    this_team = [character_map[cid_map[str(c)]] for c in teams[tname] if str(c) in cid_map and cid_map[str(c)] in character_map]
    # print([c["Name"] for c in this_team])
    # [c for c in [character_map[n] for n in character_map] if c["ID"] in teams[tname]]
    expected = sum([cid_avg_map[str(c["ID"])] for c in this_team])
    print()
    print("{} : {}".format(tname, expected))
    for c in this_team:
        print("  {} : {}".format(c["Name"], c["Average"]))
    
