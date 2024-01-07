import requests
from bs4 import BeautifulSoup as soup
from os import mkdir, getcwd, mkdir
import re

page = soup(requests.get('https://www.dataquest.io/blog/sql-commands/').content, 'html.parser')
cards = []
for el in page.find_all('h3'):
  b = el.find_next('p')
  e = el.find_next('pre')
  if (all([x is not None for x in [b, e]])):
    front = el.text
    back = b.text[len(front):]
    example = "<br />".join(e.text.split("\n"))
    print(front, back, example)
    cards.append(''.join(f'<b>Statement</b>: {front} | <b>SQL statement</b> used to{back} | {example}'))

with open(f'{getcwd()}/sql-basic.txt', 'w') as file:
  file.writelines([f'{i} \n' for i in cards])
