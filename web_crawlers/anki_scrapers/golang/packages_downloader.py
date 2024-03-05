import requests
from bs4 import BeautifulSoup as soup
from sys import argv 
from os import makedirs


def download_lib(lib='builtin', version='1.21.0'):
  page =  soup(requests.get(f'https://pkg.go.dev/{lib}@go{version}').content, 'html.parser')
  decks= {}

  for el in [i.find('span') for i in page.find_all('h4') if 'func' in i.text]:
    is_method = '(' in el.text 
    deck_name = el.text.split('(')[1].split(')')[0].replace('*', '') if is_method else 'general'
    with_options = el.find_next('div').find('pre').text
    name = el.find("a").text.strip()
    func_init = f'<i>{deck_name}</i>' if is_method else lib
    params = ', '.join([f'<i>{x.split(" ")[0]}</i>' for x in with_options.partition(name + '(')[2].split(')')[0].split(', ')])
    func = f'{func_init}.{name}({params})'
    info_start = f'<b>{lib.capitalize()} function</b> that'
    p_el = el.find_next('p')
    info_end = p_el.text[len(name) + 1:].replace('\n', ' ').split(' ') if p_el else [' ']
    info = info_start + ' ' + ' '.join(info_end)
    card = [func, info, '', with_options]
    
    if deck_name in decks.keys():
      decks[deck_name].append(card) 
    else:
      decks[deck_name] = [card]

  try:
    makedirs(lib)
  except:
    pass

  for deck, cards in decks.items():
    with open(f'{lib}/{deck}.txt', 'w') as file:
      file.writelines([f'{" | ".join(i)} \n' for i in cards])	
    
if __name__ == '__main__':
    lib, version = argv
    download_lib(lib=lib, version=version)
