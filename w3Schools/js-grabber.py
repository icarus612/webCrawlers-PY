import requests
from bs4 import BeautifulSoup as soup
from os import mkdir, getcwd, mkdir
import re

def make_folder(name): 
	try: 
		mkdir(f'{getcwd()}/{name}')
	except FileExistsError:
		pass	

home_page =  soup(requests.get('https://www.w3schools.com/jsref/default.asp').content, 'html.parser')
url_arr = [[a['href'] for a in div.find_all('a')] for div in home_page.find_all("div", {'class': 'refcont'})][0:4]
title_arr = [h2.text for h2 in home_page.find_all("h2")][0:4]
make_folder('output/')	

for idx, t in enumerate(title_arr):
	title = "".join(t.title().split())
	make_folder(f'output/{title}')	

	for url in url_arr[idx]:
		print(f'getting the content for {url}')
		cards = []
		res = soup(requests.get(f'https://www.w3schools.com/jsref/{url}.asp').content, 'html.parser')
		for table in res.find_all('table', {'class': 'ws-table-all'}):
			bold = ''
			for tr in table.find_all('tr'):
				if len(tr.find_all('th')) > 0: 
					bold = f'<b>{url.capitalize()} {tr.find("th").text.lower()}</b>'
				else:		
					ref = soup(requests.get(f'https://www.w3schools.com/jsref/{tr.find("a")["href"]}').content, 'html.parser')
					b = [i.text for i in tr.find_all('td')]
					try: 		
						back_extended = ref.find('h2', text='Syntax').findNext().findChild('div').decode_contents().strip()
						front = f'{bold}: {back_extended}'
					except Exception as e:
						back_extended = ''
						front = f'{bold}: {b[0].lower()}'
						print(e)
					back_basic = f'{bold} that {b[1].lower()}.'
					additional_info = ''
					version = ''
					try: 
						example = ref.find('div', {'class': 'w3-example'}).find('div', {'class': 'w3-code'}).decode_contents().strip()
					except AttributeError:
						example = ''
					cards.append(' '.join(f'{front} | {back_basic} | {back_extended} | {additional_info} | {example} | {version}'.splitlines()))
		with open(f'{getcwd()}/output/{title}/{url.split("_")[-1].split(".")[0]}.txt', 'w') as file:
			file.writelines([f'{i} \n' for i in cards])