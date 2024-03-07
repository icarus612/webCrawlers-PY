import requests
from bs4 import BeautifulSoup as soup
from sys import argv 
from os import makedirs


def download_commands():
	page =  soup(requests.get('https://www.ibm.com/docs/en/i/7.3?topic=extensions-standard-c-library-functions-table-by-name').content, 'html.parser')
	all_cards = [[x.text for x in i.find_all('td')] for i in page.find('tbody').find_all('tr') if len(i.find_all('td')) == 4]
	print(len(all_cards))
	deck_names = set()
	for i in all_cards:
		for d in i[1].replace('\n', ' ').split(' '):
			if len(d.strip()) > 0:
				deck_names.add(d.strip())

	decks = dict((i, []) for i in deck_names)
	for card in all_cards:
		for deck in card[1].replace('\n', ' ').split(' '):
			if deck in decks:
				decks[deck.strip()].append(card)

	try:
		makedirs('workbench')
	except:
		pass

	for deck, cards in decks.items():
		new_cards = []
		for card in cards:
			try: 
				c3 = card[2].replace('\n', ' ')
				c2 = card[3].replace('\n', ' ')
				c2 = c2[0].lower() + c2[1:]
				inner = c3.split('(')[1].split(',')
				c1 = [i.split(' ')[1] for i in c3.split(',')]
				kw = f'<b>Standard Library Function:</b> {c1}'
				info = f'<b>Standard library function</b> used to {c2}.'
				new_cards.append([kw, info, c3])
			except Exception as e:
				print(e)
				print(card)
		print(f'Writing {deck} deck...')
		with open(f'workbench/{deck}.txt', 'w') as file:
			file.writelines([f'{" | ".join(i)} \n' for i in new_cards])	
		
if __name__ == '__main__':
	download_commands()
