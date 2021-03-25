import requests
from bs4 import BeautifulSoup as soup
import json 
import sys

url = f"https://www.newegg.com/{sys.argv[1]}" if len(sys.argv) > 1 else "https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20card"
containers = soup(requests.get(url).content, 'html.parser').findAll("div", {"class": "item-container"})
obj = []

for i, x in enumerate(containers):
	title = x.find("a", {"class": "item-title"}).text.strip()
	price = x.find("li", {"class": "price-current"}).text.strip()
	shipping = x.find("li", {"class": "price-ship"}).text.strip()
	brand = x.find("a", {"class": "item-brand"}).img['src'].strip()
	deal = x.find("p", {"class": "item-promo"})
	deal = deal.text.strip() if deal.text else ""
	rating = x.find("a", {"class": "item-rating"})['title'] if x.find("a", {"class": "item-rating"}) else ""
	image = x.find("a", {"class": "item-img"}).img['src'].strip()
	id_name = "".join(title.split(" "))            	
	obj.append({"id": f"{i}",  f"{id_name}": {"title": f"{title}", "brand": f"{brand}", "price": f"{price}", "shipping": f"{shipping}", "rating": f"{rating}", "deal": f"{deal}", "image_url": f"{image}"}})

data = {"Products": []}
for i in obj:
	data['Products'].append(i)

with open("scraped.json", "w") as s:
	json.dumps(data, s)