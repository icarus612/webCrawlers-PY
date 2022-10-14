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
url_arr = [[{"url": a['href'], "title": a.text}  for a in div.find_all('a')] for div in home_page.find_all("div", {'class': 'refcont'})]
title_arr = ['Built-in Objects', 'Window', 'DOM', 'Web Api',]
make_folder('output/')	

for idx, t in enumerate(title_arr):
	title = "".join(t.split())
	make_folder(f'output/{title}')	
	for url in url_arr[idx]:
		print(f'getting the content for {url["title"]}')
		cards = []
		try:
			res = soup(requests.get(f'https://www.w3schools.com/jsref/{url["url"]}').content, 'html.parser')
		except:
			url_arr[idx]["url"].append(url)
			continue
		for table in res.find_all('table', {'class': 'ws-table-all'}):
			bold = ''
			for tr in table.find_all('tr'):
				if len(tr.find_all('th')) > 0: 
					bold = f'<b>{url["title"].capitalize()} {tr.find("th").text.lower()}</b>'
				elif tr.find('a'):		
					ref = soup(requests.get(f'https://www.w3schools.com/jsref/{tr.find("a")["href"]}').content, 'html.parser')
					b = [i.text for i in tr.find_all('td')]
					try: 		
						back_extended = ref.find('h2', text='Syntax').findNext().findChild('div').decode_contents().strip()
						front = f'{bold}: {back_extended}'
					except Exception as e:
						back_extended = ''
						front = f'{bold}: {b[0].lower()}'
						print(f'Error at {ref.find("h2", text="Syntax")}: {e}')
					back_basic = f'{bold} that {b[1].lower()}.'
					additional_info = ''
					version = ''
					try: 
						example = ref.find('div', {'class': 'w3-example'}).find('div', {'class': 'w3-code'}).decode_contents().strip()
					except AttributeError:
						example = ''
					cards.append(' '.join(f'{front} | {back_basic} | {additional_info} | {back_extended} | {example} | {version}'.splitlines()))
		with open(f'{getcwd()}/output/{title}/{"".join(url["title"].split(" "))}.txt', 'w') as file:
			file.writelines([f'{i} \n' for i in cards])