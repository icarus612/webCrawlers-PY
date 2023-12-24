import requests
import json
from sys import argv
from os import mkdir
from bs4 import BeautifulSoup as soup

def clean_txt(txt):
  nv = txt.strip().replace('~', '...').replace('〜', '...').replace('～', '...').replace('+', '...').replace('・', ' / ').replace('」', ' ').replace('「',  '')
  return nv.replace('...', ' ... ')
  
def find_td(el, val, r=True):
  return el.find('td', f'jl-td-{val}', recursive=r)

type_key = argv[1] if len(argv) > 1 else 'nouns'
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
  

for n_key, n_lst in files.items():
  for idx in range(1, 11):
    proxy_lst = []
    page = soup(requests.get(f'https://jlptsensei.com/jlpt-{n_key}-{type_key}-vocabulary-list/page/{idx}').content, 'html.parser')
    for particle in page.find_all('tr', {'class': 'jl-row'}):
      hiragana = find_td(particle, 'vr').find('p').text
      romaji = find_td(particle, 'vr').text.replace(hiragana, '') 
      info = find_td(particle, 'vm').text
      audio_name = f'ic_nrkt_{"".join(romaji.split(" "))}.mp3'
      sound = f'[sound:{audio_name}]'
      card = [clean_txt(val) for val in [hiragana, romaji, info, sound]]
      if '【' in card[1]:
        card[1] = card[1].split('【')[1].replace('】', '')
      proxy_lst.append(card)
    if len(proxy_lst) == 0:
      break
    else:
      n_lst.extend(proxy_lst)

for key, val in files.items():
  with open(f'./{type_key}/{key}.txt', 'w') as p_file:
    for card in val:
      p_file.write(" | ".join(card) + '\n')

with open(f'./{type_key}/full-list.json', 'w') as p_file:
  p_file.write(json.dumps(files))
