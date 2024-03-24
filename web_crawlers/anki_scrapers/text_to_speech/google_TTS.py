import json
import argparse

def TTS(word, language):
	pass

def load_file(file_name):
	with open(file_name, 'r') as file:
		text = file.read()
	return text

def load_json_file(file_name):
	text = load_text_file(file_name)
	return json.loads(text) 

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('file_name', default='language_file.txt', type=str, help='The name of the file to load')
	parser.add_argument('--language', '-l', default='russian', type=str, help='The language to use for the TTS')
	parser.add_argument('--version', '-v', default='A', type=str, help='The speech version to use for the TTS')
	parser.add_argument('--output', '-o', default='output', type=str, help='The name of the output file')

	args = parser.parse_args()

	if args.file_name.endswith('.json'):
		text = load_json_file(args.file_name)
	else:
		text = load_text_file(args.file_name)

	for word in text:
		TTS(word, args.language)