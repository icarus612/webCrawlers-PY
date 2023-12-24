from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
import os
from time import sleep

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
    headers = {
      'authority': 'cdn.innovativelanguage.com',
      'accept': '*/*',
      'accept-language': 'en-US,en;q=0.9',
      'cache-control': 'no-cache',
      'pragma': 'no-cache',
      'range': 'bytes=0-',
      'referer': src,
      'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Linux"',
      'sec-fetch-dest': 'video',
      'sec-fetch-mode': 'no-cors',
      'sec-fetch-site': 'same-origin',
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    audio = requests.get(src, headers=headers)
    with open(os.path.join(audio_path, name), 'wb') as audio_file:
      audio_file.write(audio.content)

def search(word_list, key_prefix=False, key_suffix=False):
	if len(word_list) == 0:
		return dict()
	def check_val(val):
		return val if val else ""

	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	audio_dict = dict()
	missed_words = []
	driver.get('https://www.japanesepod101.com/japanese-dictionary/')

	def get_word_html(el, val):
		return el.find_element(By.CLASS_NAME, f'dc-vocab_{val}').get_attribute('innerHTML')

	try:
		driver.find_element(By.CLASS_NAME, 'lightBox-signup-header-close').click()
		driver.find_element(By.CSS_SELECTOR, 'label[for="dc-search-common"]').click()
	except Exception as e: 
		print(e)

	for raw_word in word_list: 
		prefix = check_val(key_prefix)
		suffix = check_val(key_suffix)
		word = ''.join(raw_word.split(' '))
		file_path = prefix + word + suffix
		search_bar = driver.find_element(By.ID, 'dc-search-input')
		search_bar.clear()
		search_bar.send_keys(word)
		driver.find_element(By.ID, 'dc-search-button').click()
		sleep(1)
		results = driver.find_elements(By.CLASS_NAME, 'dc-result-row')
		for element in results:
			if word in [get_word_html(element, 'romanization'), get_word_html(element, 'kana')]:
				audio_dict[file_path] = element.find_element(By.TAG_NAME, 'audio').find_element(By.TAG_NAME, 'source').get_attribute('src')
		if len(results) == 0 or file_path not in audio_dict: 
			missed_words.append(raw_word)
			print(f'Error finding match for word: {raw_word}')

	return audio_dict, missed_words

def common_words(end_point='100', email=False, password=False):
	words_lst = []
	page = 1

	driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
	driver.get(f'https://www.japanesepod101.com/japanese-word-lists/?coreX={end_point}')

	try:
		driver.find_element(By.CLASS_NAME, 'lightBox-signup-header-close').click()
	except Exception as e: 
		print(e)

	try:
		driver.find_element(By.CLASS_NAME, 'js-show-sign-in-form').click()
		sleep(1)
		email = email if email else input("Enter Login Email: ")
		password = password if password else input("Enter Login Password: ")
		driver.find_element(By.CLASS_NAME, 'js-sign-in--a__email-input').send_keys(email)
		driver.find_element(By.CLASS_NAME, 'js-sign-in--a__password-input').send_keys(password)
		driver.find_element(By.CLASS_NAME, 'js-ln-sign-in-button').click()
		sleep(1)
	except Exception as e: 
		print(e)

	while True:
		print(f'Getting elements for page {page}')
		page += 1

		for element in driver.find_elements(By.CLASS_NAME, 'wlv-item'):
			item = dict()
			item['english'] = element.find_element(By.CLASS_NAME, 'wlv-item__english').get_attribute('innerHTML')
			try: 
				item['higarana'] = element.find_element(By.CLASS_NAME, 'js-wlv-word-field-kana').find_element(By.CLASS_NAME, 'wlv-item__word').get_attribute('innerHTML')
				item['romaji'] = element.find_element(By.CLASS_NAME, 'js-wlv-word-field-romaji').get_attribute('innerHTML')
				item['audio_src'] = element.find_element(By.TAG_NAME, 'audio').get_attribute('src')
				words_lst.append(item)
			except:
				print(f'Missing content for {item["english"]}')

		try: 
			driver.find_element(By.CLASS_NAME, 'r101-pagination--b').find_element(By.CSS_SELECTOR, 'a[rel="next"]').click()
			sleep(1)
		except:
			print(f'End of list at page {page}')
			break 
	
	return words_lst