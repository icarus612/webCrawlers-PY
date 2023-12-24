import requests
from bs4 import BeautifulSoup as soup
import re

cards = []
req = soup(requests.get('https://matplotlib.org/stable/api/pyplot_summary.html').content, 'lxml')
urls = [i.find('a')["href"] for i in req.select('li.toctree-l1.current')[0].find_all(class_='toctree-l2')]
for url in urls:
	try:
		url_p = url.partition('.')[2][:-5]
		print(f"Retrieving definition for {url_p}")
		full = soup(requests.get(f"https://matplotlib.org/stable/api/{url}").content, 'html5lib')
		item = full.find('dl', class_="py")
		full_m = item.find('dt', class_='sig-object')
		front = f"plt.{full_m.find('span', {'sig-name'}).text}"
		extra_info = ''
		param_type = 'property'
		if len(full_m.find_all("span", {"class": "sig-paren"})) > 0:
			param_type = 'method'
			all_args = [i.text for i in full_m.find_all(class_='sig-param')]			
			req_args = list(filter(lambda x: all([i not in ['=', '*'] for i in x]), all_args))
			if len(all_args) != len(req_args):
				extra_info = front + f"(<i>{', '.join(all_args)}</i>)"
			front += f"(<i>{', '.join(req_args)}</i>)"
		back_txt = item.find('dd').find('p').text
		back_txt = back_txt[0].lower() + back_txt[1:]
		back = f"<b>Pyplot {param_type}</b> used to {back_txt}".replace('\n', ' ')
		cards.append([front, back, '', extra_info])
	except Exception as e:
		print(e)
with open(f'matplotlib.txt', 'w') as file:
	file.writelines([f'{" | ".join(i)} \n' for i in cards])