from helpers.jpod101_crawlers import search, download_audio

def split(f, s='\t'):
  return [[i.strip() for i in x.split(s)] for x in f.readlines()]

prefix = 'ic_jp_'
suffix = '.mp3'

with open('./imported-decks/particles-new.txt') as p_new, open('./particles-final.txt', 'w') as p_final:
  final = []
  update_audio = dict()
  new = split(p_new, '|')  
  all_words = [card[1] for card in new]
  search_results = search(all_words)
  audio_dict = search_results[0]
  retry_missed = search([new[all_words.index(word)][0] for word in search_results[1]])[0]

  for key, val in retry_missed.items():
    new_key = new[[x[0] for x in new].index(key)][1]
    audio_dict[new_key] = val

  for card in new:
    if card[1] in audio_dict.keys():
      card.extend([f'[sound:{prefix}{card[1]}{suffix}]', '', ''])
      update_audio[prefix + card[1] + suffix] = audio_dict[card[1]]
      final.append(card)

  p_final.writelines([' | '.join(x) + '\n' for x in final])
  download_audio(update_audio)
