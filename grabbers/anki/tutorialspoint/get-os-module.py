import requests
from bs4 import BeautifulSoup as soup
from os import mkdir, getcwd, mkdir
import re

page =  soup(requests.get('https://tutorialspoint.com/python/os_file_methods.htm').content, 'html.parser')
cards = []
for el in page.find("table", {"class": "table-bordered"}).find_all('tr'):
	td = el.find_all('td')
	if len(td) <= 1: 
		continue
	cards.append(''.join(f'<b>Os method</b> used to {td[1].find("p").text.lower()} | {td[1].find("a").text}'))
	with open(f'{getcwd()}/output.txt', 'w') as file:
		file.writelines([f'{i} \n' for i in cards])