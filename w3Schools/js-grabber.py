import requests
from bs4 import BeautifulSoup as soup
from os import mkdir, getcwd, mkdir
import re

cards = []
url_arr = ["array", "string", "number", "math", "date", "global", "regexp", "classes", "error", "boolean", "operators", "statements", "json"]
 
for url in url_arr:
	res = soup(requests.get(f'https://www.w3schools.com/jsref/jsref_obj_{url}.asp').content, 'html.parser')
	deck_name = "JavaScript > " + url

	for table in res.find_all("table", {"class": "ws-table-all"}):
		bold = []
	
		for tr in table.find_all("tr"):
			if len(tr.find_all("th")) > 0: 
				bold = f'<b>{url.capitalize()} {tr.find("th").text}</b>'
			else:
				content = [i.text for i in tr.find_all("td")]
				front_value = f'{bold}: {content[0]}'.capitalize()
				back_value = f'{bold} that {content[1]}'.capitalize()
				cards.append(f'''
					<div id="" items"">
						<div id="" path""></div>
						<div id="" deck"">{deck_name}</div>
						<div id="" front"">{front_value}</div>
					</div>
					''' + '''
					<script>
						deck = document.getElementById(""deck""); dName = deck.innerText.split("":: "")         deck.innerHTML = dName[dName.length - 1]; document.getElementById(""path"").innerHTML = dName.join("" > ""); function addTitle(id = false, title = "" "") { let el = document.getElementById(id); if (el.innerText) { let t = document.createElement(""div""); t.classList.add(""title""); t.innerHTML = title; let b = document.createElement(""div""); b.classList.add(""body""); b.innerHTML = el.innerHTML; while (el.firstChild) { el.removeChild(el.firstChild); } el.append(t, b); } } addTitle(""front"", ""Q. ""); 
					</script> ''' + f'''
					<div id="" items"">
						<div id="" path""></div>
						<div id="" deck"">{deck_name}</div>
						<div id="" front"">{front_value}</div>
						<div id="" back"">{back_value}</div>
						<div id="" additional-info""></div>
						<div id="" options""></div>
						<div id="" example""></div> 
						<div id="" version""></div>
					</div> ''' + '''
					<script>
						deck = document.getElementById(""deck""); dName = deck.innerText.split("":: "")         deck.innerHTML = dName[dName.length - 1]; document.getElementById(""path"").innerHTML = dName.join("" > "")         version = document.getElementById(""version""); version.innerHTML = version.innerHTML || "" >= 3.7"";[...document.getElementById(""items"").children].map((el) => el.innerText ? null : el.classList.add(""hidden"")); function addTitle(id = false, title = "" "") { let el = document.getElementById(id); if (el.innerText) { let t = document.createElement(""div""); t.classList.add(""title""); t.innerHTML = title; let b = document.createElement(""div""); b.classList.add(""body""); b.innerHTML = el.innerHTML; while (el.firstChild) { el.removeChild(el.firstChild); } el.append(t, b); } } addTitle(""front"", ""Q. ""); addTitle(""back"", ""A. ""); addTitle(""options"", ""Optional Arguments: ""); addTitle(""example"", ""Example: ""); addTitle(""additional - info"", "" &#9432; ""); addTitle(""version"", ""Version: "");
					</script>
				''')
	try: 
		mkdir(f'{getcwd()}/output/')
	except FileExistsError:
		pass
	finally:
		with open(f'{getcwd()}/output/{url}.txt', 'w') as file:
			file.writelines(cards)
	