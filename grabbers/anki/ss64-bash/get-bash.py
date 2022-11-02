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
	cards.append(' '.join(f'{front} | {back_basic} | {additional_info} | {back_extended} | {example} | {version}'.splitlines()))
	with open(f'{getcwd()}/output/{title}/{"".join(url["title"].split(" "))}.txt', 'w') as file:
		file.writelines([f'{i} \n' for i in cards])