
with open('events.txt') as current_file, open('events-new.txt', 'w') as new_file:
  new_file.writelines([el.replace('<b>Window property</b>: ', 'window.') + '\n' for el in current_file.read().split('\n')])