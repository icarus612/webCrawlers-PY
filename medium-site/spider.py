from bs4 import BeautifulSoup as bs4
import requests
import sys 
import re

url = "https://medium.com"
page = requests.get(url)
body = bs4(page.text, "html.parser")
links = {a['href'] for a in body.find_all("a")} #all initial page links
old_links = [] #something to check against so we dont make requests to the same link twice
off_site_links = set()
medium_links = set()

#function for adding links to the proper lists/sets and then searching the new urls
def add_and_search(x):
	old_links.append(x)
	if re.match(r"https?://[a-zA-Z]*\.?medium\.com", x):
		medium_links.add(x)
		for j in bs4(requests.get(x).content, 'lxml').find_all("a"):
			try:
				links.add(j['href'])
			except KeyError:
				pass
	else:
		off_site_links.add(x)

try:
	looper = int(sys.argv[1]) if len(sys.argv) > 1 else 1
except ValueError:
	print("Third argument must be a number")
	quit()

for r in range(looper):
	for i in links.copy():
		if i not in old_links:
			if re.match('http', i):
				add_and_search(i)
			elif re.match('/[^/]', i):
				add_and_search(f"{url}{i}")	
		else:
			print(f"Duplicate: {i}")
	
with open('links.txt', 'w') as s:
	s.write("All page links \n")
	s.write(f"From {looper} loop(s) of mediums urls\n")
	for i in links: 
		s.write(i + '\n')
with open('stories.txt', 'w') as s:
	s.write("All story links \n")
	s.write(f"From {looper} loop(s) of mediums urls \n")
	for i in links: 
		if re.search(r'\-+\d+\-+\d+\-+', i):
			s.write(i + '\n')
with open('offSite.txt', 'w') as s:
	s.write("All off site links \n")
	s.write(f"From {looper} loop(s) of mediums urls \n")
	for i in off_site_links: 
		s.write(i + '\n')
with open('mediumLinks.txt', 'w') as s:
	s.write("All links that stay on the medium domain \n")
	s.write(f"From {looper} loop(s) of mediums urls \n")
	for i in medium_links: 
		s.write(i + '\n')