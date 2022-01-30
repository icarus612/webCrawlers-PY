import requests
from bs4 import BeautifulSoup as soup
from os import mkdir
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('url', type=str, help='Url links to convert')
parser.add_argument("-sf", "--savefile", help="Save File Name", dest='savefile', default="./convertedImages")
args = parser.parse_args()



final_string = '<div id="" items"">
	<div id="" path""></div>
	<div id="" deck"">{deck_name}</div>
	<div id="" front"">{front_value}</div>
</div>
<script>
	deck = document.getElementById(""deck""); dName = deck.innerText.split("":: "")         deck.innerHTML = dName[dName.length - 1]; document.getElementById(""path"").innerHTML = dName.join("" > ""); function addTitle(id = false, title = """") { let el = document.getElementById(id); if (el.innerText) { let t = document.createElement(""div""); t.classList.add(""title""); t.innerHTML = title; let b = document.createElement(""div""); b.classList.add(""body""); b.innerHTML = el.innerHTML; while (el.firstChild) { el.removeChild(el.firstChild); } el.append(t, b); } } addTitle(""front"", ""Q. ""); 
</script>
" "<div id="" items"">
	<div id="" path""></div>
	<div id="" deck"">{deck_name}</div>
	<div id="" front"">{front_value}</div>
	<div id="" back"">{back_value}</div>
	<div id="" additional-info"">{additional_info}</div>
	<div id="" options"">{options}</div>
	<div id="" example"">{example}</div> 
	<div id="" version"">{version} </div>
</div>
<script>
	deck = document.getElementById(""deck""); dName = deck.innerText.split("":: "")         deck.innerHTML = dName[dName.length - 1]; document.getElementById(""path"").innerHTML = dName.join("" > "")         version = document.getElementById(""version""); version.innerHTML = version.innerHTML || "" >= 3.7"";[...document.getElementById(""items"").children].map((el) => el.innerText ? null : el.classList.add(""hidden"")); function addTitle(id = false, title = """") { let el = document.getElementById(id); if (el.innerText) { let t = document.createElement(""div""); t.classList.add(""title""); t.innerHTML = title; let b = document.createElement(""div""); b.classList.add(""body""); b.innerHTML = el.innerHTML; while (el.firstChild) { el.removeChild(el.firstChild); } el.append(t, b); } } addTitle(""front"", ""Q. ""); addTitle(""back"", ""A. ""); addTitle(""options"", ""Optional Arguments: ""); addTitle(""example"", ""Example: ""); addTitle(""additional - info"", "" &#9432; ""); addTitle(""version"", ""Version: "");
</script>
'
try:
    mkdir(args.savefile)
except FileExistsError:
    pass

res = soup(requests.get(args.url).text, 'html.parser')
images = [i['src'] for i in res.find_all("img")]
print(images)
for i, x in enumerate(images):
	try: 
		req = requests.get(x)
	except:
		if args.url[-1] != '/': args.url +='/'
		req = requests.get(args.url + x)
	fileName = (re.search(r'/[^/]*\.[psj][pvn].*g?', x)).group()[1:]
	print("saving " + fileName)
	with open(f'{args.savefile}/{fileName}', 'wb') as file:
			file.write(req.content)


