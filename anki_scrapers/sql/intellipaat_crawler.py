import requests
from bs4 import BeautifulSoup as soup
from os import mkdir, getcwd, mkdir
import re

page =  soup(requests.get('https://intellipaat.com/blog/tutorial/sql-tutorial/sql-commands-cheat-sheet/').content, 'html.parser')
cards = []
for el in page.find_all('tr'):
	td = [e.text for e in el.find_all('td')]
	print(td)
	if len(td) != 3: 
		continue
	cards.append(''.join(f'<b>Statement</b>: {td[0]} | <b>SQL statement</b> used to {td[2].lower()}. | {td[1]}'))
  
with open(f'{getcwd()}/sql-basic.txt', 'w') as file:
  file.writelines([f'{i} \n' for i in cards])