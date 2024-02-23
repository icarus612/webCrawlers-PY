import requests
from bs4 import BeautifulSoup as soup
from os import mkdir
import re
import argparse



def get_images(url, savefile="./convertedImages"):
	res = soup(requests.get(url).text, 'html.parser')
	images = [i['src'] for i in res.find_all("img")]
	for i, x in enumerate(images):
		try: 
			req = requests.get(x)
		except:
			if url[-1] != '/': url +='/'
			req = requests.get(url + x)
		fileName = (re.search(r'/[^/]*\.[psj][pvn].*g?', x)).group()[1:]
		print("saving " + fileName)
		with open(f'{savefile}/{fileName}', 'wb') as file:
				file.write(req.content)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('url', type=str, help='Url links to convert')
	parser.add_argument("-sf", "--savefile", help="Save File Name", dest='savefile', default="./convertedImages")
	args = parser.parse_known_args()

	try:
		mkdir(args.savefile)
	except FileExistsError:
		pass
	get_images(args.url, args.savefile)