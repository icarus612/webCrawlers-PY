import requests
import json
import os

audio_path = 'audio/particles/ttmp3'
audio_dict = {}

with open('created-decks/particlesAudio-ttsmp3.json', 'r') as aj_file:
  audio_dict = json.loads(aj_file.read())

try:
  os.mkdir(audio_path)
except:
  pass

cookies = {
  'cookieconsent_status': 'deny',
}

headers = {
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.9',
  'Cache-Control': 'no-cache',
  'Connection': 'keep-alive',
  # 'Cookie': 'cookieconsent_status=deny',
  'Pragma': 'no-cache',
  'Range': 'bytes=0-',
  'Referer': 'https://ttsmp3.com/text-to-speech/Japanese/',
  'Sec-Fetch-Dest': 'audio',
  'Sec-Fetch-Mode': 'no-cors',
  'Sec-Fetch-Site': 'same-origin',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
  'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Linux"',
}

for name, src in audio_dict.items(): 
  audio = requests.get(src, headers=headers, cookies=cookies)
  with open(os.path.join(audio_path, name), 'wb') as audio_file:
    audio_file.write(audio.content)
