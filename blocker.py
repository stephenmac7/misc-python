#!/usr/bin/env python3
# Domain Blocker
# Run as root.
# Please, do not edit /etc/hosts until after turning off blocking.

import sys # For exiting and getting args
import re # Make sure there is not www. (added later automatically)
import shutil # To backup hosts file
from os import geteuid

def get_list():
  """Get list of things to block."""
  try:
    block_file_name = sys.argv[2]
  except IndexError:
    block_file_name = input("Block list: ")
  block_list_file = open(block_file_name, 'r')
  newlist = []
  for host in [f.replace('\n', '') for f in block_list_file.readlines()]:
    if not re.match(r'www\.[\w-]*\.\w{2,4}', host):
      newlist += [host]
  return newlist

def displayHelp():
  print("""
           Create a file with the format of:
           host1.com
           sub.host1.com
           host2.net
           sub.host2.net
           sub2.host2.net
           test.mail.com

           Then save it and run this with:
           ./blocker.py block filename.txt
           or
           python3 blocker.py block filename.txt

           You can also stop blocking by running:
           ./blocker.py unblock
           or
           python3 blocker.py unblock

           You can also replace /etc/hosts 
           with /etc/blocker_backup manually.

           If you would just like to update the block list you can run:
           ./blocker.py update filename.txt
           or
           python3 blocker.py update filename.txt
        """)

def unblock():
  """Put back old hosts file"""
  shutil.move('/etc/blocker_backup', '/etc/hosts')

def block():
  """Blocks hosts."""
  # Back up current hosts file
  shutil.copy('/etc/hosts', '/etc/blocker_backup')
  # Add new information
  hosts_file = open('/etc/hosts', 'a')
  hosts_file.write('\n#Domain Blocker Hosts\n')
  for host in get_list():
    # Write Original Hosts
    hosts_file.write('0.0.0.0\t' + host)
    # Add the www ones...
    if re.match('[\w-]*\.[\w\-.]{2,6}', host).group() == host:
      hosts_file.write(' www.' + host)
    hosts_file.write('\n')
  hosts_file.write('#Ending Blocker Hosts\n')
  hosts_file.close()

def main():
  if geteuid() != 0:
    sys.exit("Script must be run as root!")
  try:
    action = sys.argv[1]
  except IndexError:
    action = "help"
  if action == "block":
    block()
  elif action == "unblock":
    unblock()
  elif action == "update":
    unblock()
    block()
  elif action == '-h' or action == '--help' or action == 'help':
    displayHelp()

main()
