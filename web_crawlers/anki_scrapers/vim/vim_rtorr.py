import requests
from bs4 import BeautifulSoup as soup
from sys import argv 
from os import makedirs


def download_commands():
	page =  soup(requests.get('https://vim.rtorr.com/').content, 'html.parser')
	raw_decks = dict((i.text.replace(' ', '_').replace('/', ' or '), i.find_next('ul').find_all('li')) for i in page.find_all('h2') if i.find_next().name == 'ul')
	decks = dict()
	try:
		makedirs('workbench')
	except:
		pass

	for deck, items in raw_decks.items():
		cards = decks[deck] = []
		for item in items:
			txt = [i.strip() for i in item.text.split('-')]
			kw = f'<b>Vim Command:</b> {txt[0]}'
			info = f'<b>Vim command</b> used to {txt[1]}.'
			cards.append([kw, info])
   

	for deck, cards in decks.items():
		with open(f'workbench/{deck}.txt', 'w') as file:
			file.writelines([f'{" | ".join(i)} \n' for i in cards])	
		
if __name__ == '__main__':
	download_commands()
