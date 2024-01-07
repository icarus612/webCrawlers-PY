import requests
from bs4 import BeautifulSoup as soup
import re

page = soup(requests.post('https://nihongoichiban.com/home/japanese-grammar-particles/').content, 'html.parser')
elements = set([re.split(' |\xa0|\(', td.text)[0] for td in tr.find_all('td')][1] for tr in page.find_all('tr'))

print(elements)
with open('current-deck.txt') as current:
  cards = [card.split('\t') for card in current.readlines()]
  all_items = list(filter(lambda x: x[0] in elements, cards))
  print(len(all_items))