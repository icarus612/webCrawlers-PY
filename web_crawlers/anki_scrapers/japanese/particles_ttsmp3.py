from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import json
import os
from time import sleep

audio_path = 'audio/particles/ttsmp3'
audio_json = {}

def get_proxy_list():
  options = webdriver.ChromeOptions()
  options.add_argument("start-maximized")
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  options.add_experimental_option('useAutomationExtension', False)
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
  driver.get("https://sslproxies.org/")
  proxies = [[td.get_attribute('innerHTML') for td in tr.find_elements(By.TAG_NAME, 'td')][:2] for tr in driver.find_element(By.TAG_NAME, 'table').find_elements(By.TAG_NAME, 'tr')][1:]
  driver.quit()
  return [':'.join(proxy) for proxy in proxies]

try: 
	os.mkdir(audio_path)
except:
	pass

with open('./created-decks/jlptsensei-particles.json', 'r') as jlpt_json:
	raw_json = json.loads(jlpt_json.read())

caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}
options = webdriver.ChromeOptions()

for proxy in get_proxy_list():
	try:
		options.add_argument(f'--proxy-server={proxy}')
		driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()), desired_capabilities=caps)
		driver.get(f'https://ttsmp3.com/text-to-speech/Japanese/')
		driver.find_element(By.ID, 'voicetext')
		break
	except Exception as e:
		print(f'Proxy {proxy} failed, trying next...')

for deck_name, deck in raw_json.items():
	print(f'Number of audio files to create in {deck_name}: {len(deck)}')
	with open(f'./jlptsensei-particles-{deck_name}.txt', 'w') as deck_file:
		for card in deck:
			file_name = f"ic_ttmp3_{card[0].replace('...', '-').replace(' ', '').replace('/', '-')}.mp3"
			text_area = driver.find_element(By.ID, 'voicetext')
			text_area.clear()
			text_area.send_keys(card[1].split('/')[0].replace('...', '<break time="700ms"/>').strip() + '<break time="100ms"/>')
			driver.find_element(By.ID, 'vorlesenbutton').click()
			card.append(f'[sound:{file_name}]')
			sleep(5)
			browser_log = driver.get_log('performance') 
			events = [event for event in [json.loads(entry['message'])['message'] for entry in browser_log] if 'Network.response' in event['method']]

			for event in events:
				if 'response' in event["params"]:
					url = event["params"]['response']['url']
					if 'created_mp3' in url:
						audio_json[file_name] = url
			card[1], card[0] = card[:2]
			card.insert(3,  '')
			deck_file.write(' | '.join(card) + '\n')
		
with open(f'{audio_path}.json', 'w') as audio_file:
	audio_file.write(json.dumps(audio_json))
