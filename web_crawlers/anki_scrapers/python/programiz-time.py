import requests
from bs4 import BeautifulSoup as soup

res = soup(requests.get('https://www.programiz.com/python-programming/time').content, 'html.parser')

cards = [[el.text.replace('Python ', '').replace(' Function', ''), f'<b>Time method</b> used to {el.find_next("p").text}'] for el in res.find_all('h2')]

with open('time-module.txt', 'w') as time_file:
  time_file.writelines([' | '.join(card) + '\n' for card in cards])