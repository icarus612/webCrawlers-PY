import requests
from bs4 import BeautifulSoup as soup
from sys import argv 

lib = argv[1] if len(argv) > 1 else 'math'

page =  soup(requests.get(f'https://docs.python.org/3/library/{lib}.html').content, 'html.parser')
cards = []

for el in page.find_all('dl'):
	item = el.find('dt', {"class": "sig-object"})
	if item:
		u_item = item.text.strip().replace('¶', '').replace(' → int', '').replace(' → float', '').replace('(', '(<i>').replace(')', '</i>)')
		prop_type = 'method' if item.text.count('(') != 0 else 'property'
		p_el = el.find_next('p').text.replace('\n', ' ').split(' ')
		p_el[0] = p_el[0].lower()
		title = f'<b>{lib.title()} {prop_type}</b> used to ' + ' '.join(p_el)
		cards.append([title, u_item])



with open(f'{lib}.txt', 'w') as file:
	file.writelines([f'{" | ".join(i)} \n' for i in cards])	