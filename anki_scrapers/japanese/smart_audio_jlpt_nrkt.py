from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
import json
import os
from time import sleep

audio_path = 'audio/narakeet'

try: 
	os.mkdir(audio_path)
except:
	pass

files = ['nouns', 'verbs', 'adjectives', 'adverbs', 'pre-noun-adjectival']
current_lst = [el for el in os.listdir('/home/icarus-64/.local/share/Anki2/User 1/collection.media') if 'ic_nrkt_' in el]
all_lst = []

for grp in files:
  with open(f'./created-decks/jlptsensei/{grp}/full-list.json', 'r') as jlpt_json:
    elements = json.loads(jlpt_json.read())
    for v in elements.values():
      all_lst.extend(v)

fnl_lst = list(set(tuple(el) for el in all_lst if el[3].split(":")[1][:-1] not in current_lst))
fnl_lst.reverse()
#c_1 = set(c[1] for c in fnl_lst)


print(len(fnl_lst)) #768

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.narakeet.com/auth/login/')
sleep(3)
driver.find_element(By.CSS_SELECTOR, 'a[role="log-in"]').click()
sleep(20)

no_h = []

for card in fnl_lst:
  if card[0].strip() == "":
    no_h.append(card)
    continue
  file_name = card[3].split(":")[1][:-1].split('/')[0] + ".mp3"
  driver.get(f'https://www.narakeet.com/languages/japanese-text-to-speech/')
  for _ in range(8):
    sleep(1)
    try:
      format_select = Select(driver.find_element(By.ID, 'cfgAudioFormat'))
      format_select.select_by_value('mp3')
      voice_select = Select(driver.find_element(By.ID, 'cfgVideoVoice'))
      voice_select.select_by_value('yuriko')
      driver.find_element(By.CLASS_NAME, 'textarea').clear()
      driver.find_element(By.CLASS_NAME, 'textarea').send_keys(card[0].split('/')[0].replace('...', '~'))
      driver.find_element(By.NAME, 'generateaudio').click()
      break
    except Exception as e:
      print(e)

  for _ in range(8):
    sleep(5)
    status = driver.find_element(By.CSS_SELECTOR, '[data-show-stage]').get_attribute('stage').lower().strip()
    print(f'Word: {card[1]} ... {status}')
    if status == 'finished':					
      audio = requests.get(driver.find_element(By.CSS_SELECTOR, '[data-prop-link="result"]').get_attribute('href'))
      with open(os.path.join(audio_path, file_name), 'wb') as audio_file:
        audio_file.write(audio.content)
      break
    elif status == 'error':
      raise Exception('An Error Occurred')

with open('./missing-hiragana.txt', 'w') as f:
  f.writelines([" | ".join(card) for card in no_h])

print([h[1] for h in no_h])