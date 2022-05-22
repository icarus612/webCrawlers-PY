import requests
from bs4 import BeautifulSoup as soup
from os import mkdir, getcwd, mkdir
import re

# front, back, example, 
url_arr = ["array", "string", "number", "math", "date", "global", "regexp", "classes", "error", "boolean", "operators", "statements", "json"]
 
for url in url_arr[0: 1]:
	print(url)
	cards = []
	res = soup(requests.get(f'https://www.w3schools.com/jsref/jsref_obj_{url}.asp').content, 'html.parser')
	for table in res.find_all("table", {"class": "ws-table-all"}):
		bold = ""
		for tr in table.find_all("tr"):
			ref = soup(requests.get(f'https://www.w3schools.com/jsref/{table.find("a")["href"]}').content, 'html.parser')
			if len(tr.find_all("th")) > 0: 
				bold = f'<b>{url.capitalize()} {tr.find("th").text}</b>'
			else:
				content = [i.text for i in tr.find_all("td")]
				front = f'{bold}: {content[0]}'
				back_basic = f'{bold} that {content[1]}'
				back_extended = front
				additional_info = ""
				example = ref.find("div", {"class": "w3-example"}).find("div", {"class": "w3-code"})
				version = "es6"

				cards.append(f'{front} | {back_basic} | {back_extended} | {additional_info} | {example} | {version} \n')
	try: 
		mkdir(f'{getcwd()}/output/')
	except FileExistsError:
		pass	
	with open(f'{getcwd()}/output/{url}.txt', 'w') as file:
		file.writelines(cards)