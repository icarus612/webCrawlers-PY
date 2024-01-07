import requests
import json
from sys import argv
from os import mkdir
from bs4 import BeautifulSoup as soup

def clean_txt(txt):
  nv = txt.strip().replace('~', '...').replace('〜', '...').replace('～', '...').replace('+', '...').replace('・', ' / ').replace('」', ' ').replace('「',  '')
  return nv.replace('...', ' ... ')

type_key = argv[1] if len(argv) > 1 else 'particles'
files = {
  'n1': [],
  'n2': [],
  'n3': [],
  'n4': [],
  'n5': [],
}

try:
  mkdir(f'./{type_key}')
except:
  pass


for i in range(1, 11):
  proxy_lst = []
  page = soup(requests.get(f'https://jlptsensei.com/complete-japanese-{type_key}-list/page/{i}/').content, 'html.parser')
  for particle in page.find_all('tr', {'class': 'jl-row'}):
    card = [clean_txt(particle.find('td', f'jl-td-{i}').text) for i in ['gr', 'gj', 'gm', 'nl']]
    if '【' in card[1]:
      card[1] = card[1].split('【')[1].replace('】', '')
    audio_name = f'ic_nrkt_{"".join(card[0].split(" "))}.mp3'
    sound = f'[sound:{audio_name}]'
    card[0], card[1] = card[1], card[0]
    proxy_lst.append([card[3], *card[:3], sound])
  if len(proxy_lst) == 0:
    break
  else:
    for card in proxy_lst:
      files[card[0].lower()].append(card[1:])

for key, val in files.items():
  with open(f'./{type_key}/{key}.txt', 'w') as p_file:
    for card in val:
      p_file.write(" | ".join(card) + '\n')

with open(f'./{type_key}/full-list.json', 'w') as p_file:
  p_file.write(json.dumps(files))
