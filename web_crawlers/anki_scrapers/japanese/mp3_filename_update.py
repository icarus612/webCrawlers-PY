import requests
import json
import os

all_lst = [el for el in os.listdir('/home/icarus-64/.local/share/Anki2/User 1/collection.media') if 'ic_nrkt_' in el]
update_lst = [el for el in all_lst if '.mp3' not in el]

print(all_lst)
print(update_lst)

files = ['nouns', 'verbs', 'adjectives', 'adverbs', 'pre-noun-adjectival', 'particles']
grps = {
  'n1': {},
  'n2': {},
  'n3': {},
  'n4': {},
  'n5': {},
}

for grp in files:
  with open(f'./created-decks/jlptsensei/{grp}/full-list.json', 'r') as jlpt_json:
    elements = json.loads(jlpt_json.read())
    for k, v in elements.items():
      grps[k][grp] = len(v)

for k, v in grps.items():
  print(k)
  for k2, v2 in v.items():
    print(k2, v2)