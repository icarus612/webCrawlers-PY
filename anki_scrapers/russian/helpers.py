import requests
import os
from bs4 import BeautifulSoup as soup


def download_audio(audio_dict, audio_path='audio_files', wipe_old=False): 
	try: 
		os.mkdir(audio_path)
	except:
		if wipe_old: 
			for root, dirs, files in os.walk(audio_path, topdown=False):
				for name in files:
						os.remove(os.path.join(root, name))
				for name in dirs:
						os.rmdir(os.path.join(root, name))

	for name, src in audio_dict.items(): 
		print(f'Downloading {name}...')
		headers = {
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
				'Accept-Language': 'en-US,en;q=0.9',
				'Cache-Control': 'max-age=0',
				'Connection': 'keep-alive',
				'If-Modified-Since': 'Mon, 21 Jun 2010 09:05:09 GMT',
				'If-None-Match': '"4683ed92011cb1:0"',
				'Range': 'bytes=0-11689',
				'Upgrade-Insecure-Requests': '1',
				'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
		}
		audio = requests.get(src, headers=headers)
		with open(os.path.join(audio_path, name), 'wb') as audio_file:
			audio_file.write(audio.content)

def get_audio_src(u):
	url = u if u.startswith('http') else f'http://masterrussian.com{u}'
	print(f'Attempting to get audio src for {url}')
	return soup(requests.get(url).content, 'html.parser').find('audio', {'id': 'audioplayer'})['src']

	
	return r

def get_page_words(page=''):
		url = f'http://masterrussian.com/vocabulary/most_common_words{page}.htm'
		content = soup(requests.get(url).content, 'html.parser')
		words_lst = []
		
		for element in content.find('table', {'class': 'topwords'}).find_all('tr')[1:]:
			item = dict()
			try:
				russian_el = element.find('td', {'class': 'word'})
				print(f'Attempting to create card for {russian_el.text.strip()}')
				audio_url = russian_el.find('a') or dict()
				item['audio_src'] = get_audio_src(audio_url.get('href'))
				td = element.find_all('td')
				r_idx = td.index(russian_el)
				td_txt = [i.text.strip() for i in td][r_idx:]
				item['russian'] = td_txt[0]
				item['pos'] = td_txt[1]
				item['english'] = td_txt[2]
				item['file_name'] = f'ic_mr_{item["russian"].replace(" ", "_")}.mp3'
				words_lst.append(item)
				print('Card created...\n')
			except Exception as e:
				print('A error occurred:')
				print(e, '\n')
		return words_lst
	
def build_cards(grp):
	with open(f'./master-russian.txt', 'w') as f_grp:
		f_grp.writelines(f'{card["russian"]} | {card["pos"]} | {card["english"]} | [sound:{card["file_name"]}] \n' for card in grp)
	
def build_cw_deck():
	cards_lst = []
	
	for page in ['', *[f'_{i}' for i in range(2, 13)]]:
		print(f'Getting elements for page {page[1:] or 1}\n')
		new_cards = get_page_words(page)
		cards_lst.extend(new_cards)
	
	build_cards(cards_lst)
	file_urls = dict([(i['file_name'], i['audio_src']) for i in cards_lst if i['audio_src'] is not None])
	download_audio(file_urls, audio_path='./audio_files')