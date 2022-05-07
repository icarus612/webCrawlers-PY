import requests
from bs4 import BeautifulSoup as soup
from os import mkdir
import re

content = []
url_arr = ["array", "string", "number", "math", "date", "global", "regexp", "classes", "error", "boolean", "operators", "statements", "json"]
 
for item in url_arr:
	res = soup(requests.get(f'https://www.w3schools.com/jsref/jsref_obj_{item}.asp').html, 'html.parser')
	tr = res.find_all("tr")
	print(tr)
	deck_name = ""
	front_value = ""
	back_value = ""
	additional_info = ""
	options = ""
	example = "" 
	version = ""

	#content.append(f"""
	#	<div id="" items"">
	#		<div id="" path""></div>
	#		<div id="" deck"">{deck_name}</div>
	#		<div id="" front"">{front_value}</div>
	#	</div>
	#	<script>
	#		deck = document.getElementById(""deck""); dName = deck.innerText.split("":: "")         deck.innerHTML = dName[dName.length - 1]; document.getElementById(""path"").innerHTML = dName.join("" > ""); function addTitle(id = false, title = "" "") { let el = document.getElementById(id); if (el.innerText) { let t = document.createElement(""div""); t.classList.add(""title""); t.innerHTML = title; let b = document.createElement(""div""); b.classList.add(""body""); b.innerHTML = el.innerHTML; while (el.firstChild) { el.removeChild(el.firstChild); } el.append(t, b); } } addTitle(""front"", ""Q. ""); 
	#	</script>
	#	<div id="" items"">
	#		<div id="" path""></div>
	#		<div id="" deck"">{deck_name}</div>
	#		<div id="" front"">{front_value}</div>
	#		<div id="" back"">{back_value}</div>
	#		<div id="" additional-info"">{additional_info}</div>
	#		<div id="" options"">{options}</div>
	#		<div id="" example"">{example}</div> 
	#		<div id="" version"">{version}</div>
	#	</div>
	#	<script>
	#		deck = document.getElementById(""deck""); dName = deck.innerText.split("":: "")         deck.innerHTML = dName[dName.length - 1]; document.getElementById(""path"").innerHTML = dName.join("" > "")         version = document.getElementById(""version""); version.innerHTML = version.innerHTML || "" >= 3.7"";[...document.getElementById(""items"").children].map((el) => el.innerText ? null : el.classList.add(""hidden"")); function addTitle(id = false, title = "" "") { let el = document.getElementById(id); if (el.innerText) { let t = document.createElement(""div""); t.classList.add(""title""); t.innerHTML = title; let b = document.createElement(""div""); b.classList.add(""body""); b.innerHTML = el.innerHTML; while (el.firstChild) { el.removeChild(el.firstChild); } el.append(t, b); } } addTitle(""front"", ""Q. ""); addTitle(""back"", ""A. ""); addTitle(""options"", ""Optional Arguments: ""); addTitle(""example"", ""Example: ""); addTitle(""additional - info"", "" &#9432; ""); addTitle(""version"", ""Version: "");
	#	</script>
	#""")

with open('output.txt', 'wb') as file:
		file.writelines(content)
	