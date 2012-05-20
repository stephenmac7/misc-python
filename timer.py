#!/usr/bin/env python3
# Imports
from os import system
from sys import argv
# Functions
def getLongName(type):
  if type == "m":
    longname = "Minutes"
  elif type == "s":
    longname = "Seconds"
  elif type == "h":
    longname = "Hours"
  elif type == "d":
    longname = "Days"
  else:
    print("Sorry, that was not a valid type.")
    exit()
  return longname
def getUserTime():
  type = input("Timing type(s/m/h): ").lower()
  try:
    time = float(input("Time: "))
  except TypeError:
    print("Sorry, that was not a valid option.")
    exit()
  longname = getLongName(type)
  return time, type, longname

# Variables
sofar = 0
time, type, longname = getUserTime()
## Get interval
if argv[1:]:
  interval = float(argv[1])
  if time % interval != 0:
    print("WARNING: Your custom interval is not optimal and",
          "the computer may count over!")
else:
  interval = time/10
# Print Interval
print("We'll be counting in intervals of", interval, longname)
# Create System Command
systemcommand = "sleep " + str(interval) + str(type)
# Run the loop
while sofar < time:
  system(systemcommand)
  sofar += interval
  print("We have gone", round(sofar, 2), longname, "so far.")
# Make sure the user remembers they've finished.
print("Finished!")
