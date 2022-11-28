import requests
from bs4 import BeautifulSoup as soup
from os import mkdir, getcwd, mkdir
import re

with open(f'{getcwd()}/home.html') as home:
	page = soup(home, 'html.parser')
	cards = []
	for idx, el in enumerate(page.find_all('h3', {'class': 'fittexted_for_content_h3'})):
		next_el = el.find_next().text
		definition = f'<b>Os method</b> used to {next_el[0].lower() + next_el[1:]}.'
		method = f'os.{el.text.split(" ")[1]}'
		cards.append(f'{definition} | {method} | | {method}' )
		with open(f'{getcwd()}/output.txt', 'w') as file:
			file.writelines([f'{i} \n' for i in cards])