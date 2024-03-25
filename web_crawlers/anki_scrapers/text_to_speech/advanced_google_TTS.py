import json
import argparse
import os
from google_speech import Speech
from retrying import retry

@retry(wait_exponential_multiplier=1000, wait_exponential_max=40000)
def TTS(word, language):
	return Speech(word, language)

def load_file(file_name):
	with open(file_name, 'r') as file:
		text = file.readlines()
	return text

def load_json_file(file_name):
	with open(file_name, 'r') as file:
		text = file.read()	
	return json.loads(text) 

def save_speech_audio(file_name, audio, replace=True):
	if replace or not os.path.isfile(file_name):
		Speech.save(audio, file_name)

def build_and_save(word, language, file_name=None, dir_name='audio_files', replace=True):
	if not os.path.isdir(dir_name):
		os.mkdir(dir_name)

	if not file_name:
		file_name = os.path.join(dir_name, f'{word.replace(" ", "_")}_{language}.mp3')
	audio = TTS(word, language)
	save_speech_audio(file_name, audio, replace=replace)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--word', '-w', type=str, help='The word to load')
	parser.add_argument('--file', '-f', type=str, help='The name of the file to load')
	parser.add_argument('--language', '-l', default='RU', type=str, help='The language to use for the TTS')
	parser.add_argument('--output_dir', '-o', default='audio_files', type=str, help='The name of the output file')
	parser.add_argument('--split_char', '-s', default='|', type=str, help='The name of the output file')
	args = parser.parse_args()

	if args.word:
		build_and_save(args.word, args.language, dir_name=args.output_dir)

	elif args.file:
		if args.file.endswith('.json'):
			cards = load_json_file(args.file_name).items()
		else:
			cards = load_file(args.file_name)
			if args.split_char:
				cards = [i.split(args.split_char) for i in cards]
	
		for card in cards:
			if len(card) == 1:
				build_and_save(word, args.language, dir_name=args.output_dir) 
			else:
				build_and_save(word, args.language, file_name=file, dir_name=args.output_dir) 
		