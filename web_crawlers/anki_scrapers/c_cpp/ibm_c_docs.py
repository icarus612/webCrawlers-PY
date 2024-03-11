import requests
from bs4 import BeautifulSoup as soup
from sys import argv 
from os import makedirs


def download_commands():
	page =  soup(requests.get('https://www.ibm.com/docs/en/i/7.3?topic=extensions-standard-c-library-functions-table-by-name').content, 'html.parser')
	all_cards = [i.find_all('td') for i in page.find('tbody').find_all('tr') if len(i.find_all('td')) == 4]
	deck_names = set()
	for i in all_cards:
		for d in i[1].text.replace('\n', ' ').split(' '):
			if len(d.strip()) > 0:
				deck_names.add(d.strip())

	decks = dict((i, []) for i in deck_names)
	for card in all_cards:
		for deck in card[1].text.replace('\n', ' ').split(' '):
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
				c1 = card[2].decode_contents().replace('\n', ' ').replace('em>', 'i>')
				c2 = card[3].text.replace('\n', ' ')
				c2 = c2[0].lower() + c2[1:]
				deck_name = deck.split('.')[0].capitalize()
				kw = f'<b>{deck_name} Function:</b> {c1}'
				info = f'<b>{deck_name} function</b> used to {c2}'
				new_cards.append([kw, info])
			except Exception as e:
				print(e)
				print(card)
		print(f'Writing {deck} deck...')
		with open(f'workbench/{deck}.txt', 'w') as file:
			file.writelines([f'{" | ".join(i)} \n' for i in new_cards])	
		
if __name__ == '__main__':
	download_commands()
