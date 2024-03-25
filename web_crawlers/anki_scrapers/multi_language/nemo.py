import requests
from bs4 import BeautifulSoup as soup
from sys import argv 
from os import makedirs


def crawl_page(language, output_file='output.txt', audio_dir='audio_files'):
  page =  soup(requests.get(f'http://www.nemolanguageapps.com/phrasebooks/{language}').content, 'html.parser')

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

  if os.

  for deck, cards in decks.items():
    with open(f'{lib}/{deck}.txt', 'w') as file:
      file.writelines([f'{" | ".join(i)} \n' for i in cards])	
    
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('language', default='russian', type=str, help='The language to use for the TTS')
	parser.add_argument('--output_file', '-o', default='output.txt', type=str, help='The name of the output file')
	parser.add_argument('--audio_dir', '-d', default='audio_files', type=str, help='The name of the output file')
	parser.add_argument('--split_char', '-s', default='|', type=str, help='The name of the output file')
	args = parser.parse_args()    
	
	crawl_page(ards.language, output_file=args.output_file, audio_dir=args.audio_dir)
