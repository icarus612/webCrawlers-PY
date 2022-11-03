import requests
from bs4 import BeautifulSoup as soup
from os import mkdir, getcwd, mkdir
import re

page =  soup(requests.get('https://ss64.com/bash/').content, 'html.parser')
cards = []
for el in page.find_all('tr'):
	td = list(filter(lambda x: x != "\xa0", [e.text for e in el.find_all('td')]))
	if len(td) == 1: 
		continue
	cards.append(''.join(f'<b>Command</b>: {td[0]} | <b>Bash command</b> to {td[1].lower()}'))
	with open(f'{getcwd()}/output.txt', 'w') as file:
		file.writelines([f'{i} \n' for i in cards])