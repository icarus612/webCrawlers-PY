def split(deck): 
  return [line.split('\t') for line in deck.readlines()]

new_items = set()
decks_path = './current-decks'
output_path = './workbench'

with open(f'{decks_path}/kana-alphabet.txt') as vocab, open(f'{decks_path}/kana-alphabet.txt') as words, open("./particles-full.txt") as cards, open("./particles-final.txt", "w") as final:   
  new_cards = split(cards)
  new_vocab = split(vocab)
  new_words = split(words)

  for card in new_cards:
    card[4] = False
    for w in new_words:
      if any(bool(i) and i in card for i in w[:3]):
        card[4] = w[3]
        new_items.add(card[0])
    
    for v in new_vocab:
      if v[1] in card:
        card[4] = v[2]
        new_items.add(card[0])
      elif v[0] in card and not bool(card[4]): 
        card[4] = v[2]
        new_items.add(card[0])
    
  final.writelines(["\t".join(card) for card in new_cards])