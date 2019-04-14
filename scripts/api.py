#!/usr/bin/env python3

import json
import requests

CHAR_OVERVIEW_URL = "https://fantasora.com/api/char/{}?seasonId=68"
CHAR_SCORES_URL = "https://fantasora.com/api/scores?charId={}&rulesetId=14"
CHAR_EVENTS_URL = "https://fantasora.com/api/event?charId={}&rulesetId=14"

def _clean(x):
    if isinstance(x, str):
        return x.replace("\t","").strip()
    return x

def _request(url_base, char_id):
    data = requests.get(url_base.format(char_id)).json()
    data = {k:_clean(data[k]) for k in data}
    return data

def get_character_overview(char_id):
    return _request(CHAR_OVERVIEW_URL, char_id)

def get_character_scores(char_id):
    return _request(CHAR_SCORES_URL, char_id)

def get_character_events(char_id):
    return _request(CHAR_EVENTS_URL, char_id)


# character = 31
# print(json.dumps(get_character_overview(character), indent=2, sort_keys=True))
# print(json.dumps(get_character_scores(character), indent=2, sort_keys=True))
