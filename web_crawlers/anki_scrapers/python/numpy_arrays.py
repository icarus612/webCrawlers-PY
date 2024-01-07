import requests
from bs4 import BeautifulSoup as soup
import re

cards = []
req = soup(requests.get('https://numpy.org/doc/stable/reference/arrays.ndarray.html').content, 'html.parser')

urls = [i.find('a')["href"] for i in req.find_all(class_='toctree-l3')]


for url in urls:
	try:
		url_p = url.partition('.')[2][:-5]
		if re.search(r'__\w*__', url_p):
			continue
		print(f"Retrieving definition for {url_p}")
		full = soup(requests.get(f"https://numpy.org/doc/stable/reference/{url}").content, 'html.parser')
		item = full.find('dl', class_="py")
		full_m = item.find('dt', class_='sig-object')
		front = f"<i>ndarray</i>.{full_m.find('span', {'sig-name'}).text}"
		extra_info = ''
		param_type = 'property'
		if 'method' in [i.text for i in full.find_all('p')]:
			param_type = 'method'
			all_args = [i.text for i in full_m.find_all(class_='sig-param')]			
			req_args = [x for x in all_args if '=' not in x]
			if len(all_args) != len(req_args):
				extra_info = front + f"(<i>{', '.join(all_args)}</i>)"
			front += f"(<i>{', '.join(req_args)}</i>)"
		
		back_txt = item.find('dd').find('p').text
		back_txt = back_txt[0].lower() + back_txt[1:]
		back = f"<b>Ndarray {param_type}</b> used to {back_txt}".replace('\n', ' ')
		back = back[0].lower() + back[1:]
		cards.append([front, back, '', extra_info])
	except Exception as e:
		print(e)
with open(f'numpy_arrays.txt', 'w') as file:
	file.writelines([f'{" | ".join(i)} \n' for i in cards])