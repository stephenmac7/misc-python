#!/usr/bin/env python3

# Imports
import argparse, sys, re

# Functions
def parseLines(lines, rFrom, rTo, regex, removeNL = False):
  """ Takes lines and replaces text and if selected, removes newline characters. """
  # Loop through lines
  for line in lines:
    newline = line
    # If selected, remove newline characters
    if removeNL:
      newline = line.replace('\n', '')
    # If line has the selected text or regex, replace it with the target text
    if regex:
      for match in re.findall(rFrom, newline):
        newline = newline.replace(match, rTo)
    else:
      if rFrom in newline:
        newline = newline.replace(rFrom, rTo)
    lines[lines.index(line)] = newline
  return lines

# Get command arguments and if present, pipe info
cmdParser = argparse.ArgumentParser()
cmdParser.add_argument("rFrom", help="Search for, to replace.")
cmdParser.add_argument("rTo", help="Replace with.")
cmdParser.add_argument("-p", "--pipe", help="Take data from Pipe.", action="store_true")
cmdParser.add_argument("-w", "--write", help="Write data to input file.", action="store_true")
cmdParser.add_argument("-i", "--input", help="Input file.", default="none")
cmdParser.add_argument("-r", "--regex", help="Use python regex for lines to replace.", action="store_true")
args = cmdParser.parse_args()
# Check for input.
if not args.pipe and args.input == "none":
  print("You must have an input!")
  sys.exit(256)
# If there is one...
else:
  # If the user wants the pipe to be the input...
  if args.pipe:
    lines = sys.stdin.readlines()
    # The problem with arguemnts...
    if args.write:
      print("Sorry, since you have piped data to the software there is no place to write! We will write to stdout.")
  else:
    # Open file and read it
    f = open(args.input, 'r+')
    lines = f.readlines()
    # Go back to the beginning
    f.seek(0)
if not args.write:
  for line in parseLines(lines, args.rFrom, args.rTo, args.regex, True):
    print(line)
else:
  f.writelines(parseLines(lines, args.rFrom, args.rTo, args.regex))
