
with open('sys-module.txt', 'w') as sys_file:
  sys_file.writelines([f'sys.{item} | <b>Sys property</b> used to \n'for item in ['stdin', 'stdout', 'stderr', 'argv', 'path', 'modules']])