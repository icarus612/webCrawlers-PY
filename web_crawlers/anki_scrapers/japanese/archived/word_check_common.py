particles = []

def get_el(el, idx=0):
  return el.split('|')[idx].strip()

for i in range(1, 11):
  with open(f'./created-decks/jp101-core-{i}00.txt') as deck:
    particles.append(set(el for el in deck.readlines()))

for idx, deck in enumerate(particles):
  r = []
  a = []
  for i, x in enumerate(particles):
    if i != idx:
      r.extend([get_el(e) for e in x])
      a.extend(x)
  
  itr = [(get_el(card, 1), get_el(card, 2)) for card in deck if get_el(card) in r and card not in a]
  #print(len(itr))
  print(itr)

