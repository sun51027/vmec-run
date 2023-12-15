import sys, os

from multiprocessing import Process

def run(command, nice=True):
  ''' /bin/nice is used to lower the priority of a command if enabled '''
  print("Command is ", command)
  if nice:
    os.system("/bin/nice -n 19 " + command)
  else:
    os.system(command)
  return

def submit_jobs(command_list, n_par, nice=True):
  '''
  n_par = number of parallel jobs

  Submitting jobs until n_par of them are running in the same time.
  A finished job will be remove from the list and another one will be put in queue.
  If the total number of jobs is smaller than n_par, it will check number of remaining jobs in another while loop.
  '''
  nice = False # bypass a system issue about lacking of /bin/nice
  running_procs = []
  for command in command_list:
    running_procs.append(Process(target=run, args=(command,nice,)))
    running_procs[-1].start()
    while True:
      for i in range(len(running_procs)):
        if not running_procs[i].is_alive():
          running_procs.pop(i)
          break
      if len(running_procs) < n_par:
        break
      else:
        os.system("sleep 5s")
  while len(running_procs) > 0:
    for i in range(len(running_procs)):
      try:
        if not running_procs[i].is_alive():
          running_procs.pop(i)
      except:
        continue
