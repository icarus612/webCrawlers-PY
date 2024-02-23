
import requests
import sys
import argparse

def get_audio(path, url, **kwargs):
	audio = requests.get(url, headers=kwargs['headers'], cookies=kwargs['cookies'])
	with open(path, 'wb') as audio_file:
		audio_file.write(audio.content)

if __name__ == '__main__':
  
	parser = argparse.ArgumentParser()
	parser.add_argument('audio_path', type=str, help='Path to audio file to save to.')
	parser.add_argument('url', type=str, help='URL to convert audio src of.')
	parser.add_argument("-h", "--headers", help="URL headers (if needed)", dest='headers', type=dict)
	parser.add_argument("-c", "--cookies", help="URL cookies (if needed)", dest='cookies', type=dict)

	args = parser.parse_known_args()
	get_audio(args.audio_path, args.url, headers=args.headers, cookies=args.cookies)