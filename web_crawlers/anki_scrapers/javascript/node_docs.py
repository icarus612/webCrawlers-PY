import requests
from bs4 import BeautifulSoup as soup
from sys import argv 

lib = argv[1] if len(argv) > 1 else 'path'
should_remove_start = len(argv) <= 2  or argv[2].lower() not in ['0', 'false', 'f', 'n', 'no']
page =  soup(requests.get(f'https://nodejs.org/api/{lib}.html').content, 'html.parser')
cards = []

header = list(filter(lambda x: any([len(i.find_all('code')) > 0 for i in x]), [page.find_all(f'h{i}') for i in range(3, 6)]))[0]
for el in header:
  item = el.find('code')
  if item:
    u_item = item.text.strip().replace('(', '(<i>').replace(')', '</i>)').replace('<i></i>', '')
    prop_type = 'method' if '(' in u_item else 'property'
    title = f'<b>{lib.title()} {prop_type}</b> used to'

    for sib in el.next_siblings:
      match sib.name:
        case 'p':
          part = u_item.partition("(")[0] + ") " if prop_type == 'method' else u_item
          cut_len = len(f'The {part} {prop_type} ') if should_remove_start else 0
          add_title = sib.text.replace('\n', '')[cut_len:].strip().split(' ')
          add_title[0] = add_title[0].lower()
          if len(add_title[0]) > 0 and add_title[0][-1] == 's': 
            add_title[0] = add_title[0][:-1]
          title = ' '.join([*title.split(' '), *add_title])
        case 'h1' | 'h2' | 'h3' | 'h4' | 'h5':
          break

    cards.append([title, u_item])

with open(f'{lib}.txt', 'w') as file:
  file.writelines([f'{" | ".join(i)} \n' for i in cards])	