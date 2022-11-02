import requests
from bs4 import BeautifulSoup as soup
from os import mkdir, getcwd, mkdir
import re

def make_folder(name): 
	try: 
		mkdir(f'{getcwd()}/{name}')
	except FileExistsError:
		pass	

page =  soup(requests.get('https://ss64.com/bash/').content, 'html.parser')
make_folder('output/')	
cards = []
for el in page.find_all('tr'):
	td = el.find_all('td')
	cards.append(' '.join(f'{td[1]} | {td[2]}'))
	with open(f'{getcwd()}/output.txt', 'w') as file:
		file.writelines([f'{i} \n' for i in cards])