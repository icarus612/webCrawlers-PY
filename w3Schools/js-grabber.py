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
			if len(tr.find_all("th")) > 0: 
				bold = f'<b>{url.capitalize()} {tr.find("th").text}</b>'
			else:		
				ref = soup(requests.get(f'https://www.w3schools.com/jsref/{tr.find("a")["href"]}').content, 'html.parser')
				b = [i.text for i in tr.find_all("td")]
				try: 		
					back_extended = ref.find("h2", text="Syntax").findNext().findChild("div").findChild("div")
					front = f'{bold}: {back_extended}'
				except Exception as e:
					back_extended = ""
					front = f'{bold}: {b[0]}'
					print(e)

				back_basic = f'{bold} that {b[1]}'
				additional_info = ""
				example = ref.find("div", {"class": "w3-example"}).find("div", {"class": "w3-code"})
				version = "es6"

				cards.append(" ".join(f'{front} | {back_basic} | {back_extended} | {additional_info} | {example} | {version}'.splitlines()))
	try: 
		mkdir(f'{getcwd()}/output/')
	except FileExistsError:
		pass	
	
	print(cards[0])
	with open(f'{getcwd()}/output/{url}.txt', 'w') as file:
		file.writelines(cards)