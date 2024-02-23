import sys
import requests
import re
from bs4 import BeautifulSoup as bs4

def get_js(url):
	link = bs4(requests.get(url).text).find_all("script")
	on_page = []
	off_page = []
	for i in link:
		try:
			off_page.append(i['src'])
		except KeyError: 
			on_page.append(i)

	with open('jsOnPage.js', 'w') as js:
		js.write('// All the JavaScript on the page. \n\n')
		for i in on_page:
			js.write(i.text + "\n")

	with open('thirdPartyJS.js', 'w') as js:
		js.write('// All third party Javascript. \n\n')
		for i in off_page:
			if re.match(r'http', i) and not re.match(sys.argv[1], i):
				js.write(requests.get(i).text + "\n")

	with open('jsOffPage.js', 'w') as js:
		js.write('// All the JavaScript off the page. \n\n')
		for i in off_page:
			if re.match(r'/', i):
				js.write(requests.get(f"{sys.argv[1]}{i}").text + "\n")
			elif re.match(r'./', i):
				js.write(requests.get(f"{sys.argv[1]}{i[1:]}").text + "\n")
			elif not re.match(r'http', i): 
				js.write(requests.get(f"{sys.argv[1]}/{i}").text + "\n")

if __name__ == "__main__":
	get_js(sys.argv[1])