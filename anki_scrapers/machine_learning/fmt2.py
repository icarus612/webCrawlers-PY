f = dict()
t = dict()
c = ''

with open('./unique-terms.txt', 'r') as u:	
  for line in u.readlines():
    if ':' in line:
      c = line.strip()[:-1]
      f[c] = []  
    elif line.strip() != '':
      f[c].append(line.strip())

with open('./all-terms.txt', 'r') as a:
  for i in a.readlines():
    k, v = i.split(' | ')
    t[k] = v
    
for k, v in f.items():
  with open(f'sorted/{k.replace(" ", "-")}.txt', 'w') as final:
    final.writelines([f'{i} | {t[i]}' for i in v if i in t])
    
for l in f.values():
  for v in l:
    if v in t.keys():
      del t[v] 
    
with open('./missing-terms.txt', 'w') as missing:
    missing.writelines([k + '\n' for k in t.keys()])
