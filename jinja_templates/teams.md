## Character points:
{% for char in characters %}
### {{char['place']}}: [{{char['name']}}]({{char['link']}}) ({{char['avg_points']}} pps)
<details>
<summary> {{char['total_points']}} total points in {{char['season_count']}} season{{'s' if char['season_count'] > 1 else ''}} </summary>
{% for season in char['seasons'] %}<details>
<summary>Season {{ season['number'] }}: {{ season['total'] }}</summary>

[Fantasora link]({{season['link']}})  {% for ctg in season['categories'] %}
**{{ ctg }}** : {{ season['categories'][ctg] }}  {% endfor %}
</details>
{% endfor %}
</details>
{% endfor %}
