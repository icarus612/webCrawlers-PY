import requests
from bs4 import BeautifulSoup as soup
from os import mkdir
import re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('url', type=str, help='Url links to convert')
parser.add_argument("-sf", "--savefile", help="Save File Name", dest='savefile', default="./convertedImages")
args = parser.parse_args()

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