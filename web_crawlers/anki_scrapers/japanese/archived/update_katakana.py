def split(f):
  return [x.split('\t') for x in f.readlines()]

with open("hiragana.txt", "r") as hf, open("katakana.txt", "r") as kf, open("workbench.txt", "w") as of:
  h = split(hf)
  k = split(kf)
  new_items = []

  for card in k:
    try:
      card[1] = list(filter(lambda x: card[1] in x, h))[0][1]
    except:
      print("Card not found")
    
    of.write(" | ".join(card))

