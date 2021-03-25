import requests
from bs4 import BeautifulSoup as soup
import json 

res = requests.get("https://store.steampowered.com").content
page = soup(res, 'lxml')
containers = page.find_all("a", {"class": "store_capsule"})
obj = []

for i, x in enumerate(containers):
	id_to_find = x['data-ds-appid']
	title = page.find("div", {"id": f"hover_app_{id_to_find}"}).find("h4").text if page.find("div", {"id": f"hover_app_{id_to_find}"}) != None else id_to_find
    price_bd = x.find("div", {"class": "discount_origional_price"}) else ""
	if x.find("div", {"class": "discount_pct"}):
		price_ad = x.find("div", {"class": "discount_final_price"}).text.strip() if x.find("div", {"class": "discount_final_price"}) else ""
		deal_pct = x.find("div", {"class": "discount_pct"}).text.strip() if x.find("div", {"class": "discount_pct"}) else ""
	else:
		price_ad = price_bd
		deal_pct = "0%"
	image = x.find('img')['src']
	time_left = x.find('dailydeal_desc').text if x.find('dailydeal_desc') else "NA"	
	id_name = "".join(title.split(" "))   
	obj.append({"id": f"{i}",  f"{id_name}" : {"title": f"{title}", "price before deal": f"{price_bd}", "price after deal": f"{price_ad}", "deal percent": f"{deal_pct}", "image_url": f"{image}", "time left" : f"{time_left}"}})


data = {"Products": []}
for i in obj:
	data['Products'].append(i)

with open ("scraped.json", 'w') as s:
	json.dumps(data, s)