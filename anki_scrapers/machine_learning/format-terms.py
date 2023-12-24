with open('./all-terms.txt', 'w') as t, open('./neural-networks-types.txt', 'r') as u:	
  n = []
  f = []
  for i, line in enumerate(u.readlines()):
    match i % 3:
      case 0:
        n.append(f)
        f = []
      case 1: 
        continue
    f.append(line.replace(':', ' ').strip())
        
	  
  t.writelines([' | '.join(i) + '\n' for i in n])