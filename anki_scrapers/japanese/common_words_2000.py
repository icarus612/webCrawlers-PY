from helpers.jpod101_crawlers import common_words, download_audio

def split(f, s='\t'):
  return [[i.strip() for i in x.split(s)] for x in f.readlines()]

prefix = 'ic_jp_'
suffix = '.mp3'
audio_dict  = dict()

def build_cards(val, grp):
  with open(f'./jp101-core-{val}.txt', 'w') as f_grp:
    for card in grp:
      file_name = prefix + "_".join(card["romaji"].split(" ")) + suffix
      f_grp.writelines(f'{card["higarana"]} | {card["romaji"]} | {card["english"]} | [sound:{file_name}] \n')
      audio_dict[file_name] = card['audio_src']

cards = common_words('2000')
build_cards(f'{idx + 1}00', cards)
download_audio(audio_dict)