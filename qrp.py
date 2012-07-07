#!/usr/bin/env python3

# Imports
import argparse, sys, re

# Functions
def parseLines(lines, rFrom, rTo, regex, oline, removeNL = False):
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
        if not oline:
          newline = newline.replace(match, rTo)
        else:
          newline = rTo
    else:
      if rFrom in newline:
        if not oline:
          newline = newline.replace(rFrom, rTo)
        else:
          newline = rTo
    lines[lines.index(line)] = newline
  return lines

# Get command arguments
cmdParser = argparse.ArgumentParser()
# Must have the following
cmdParser.add_argument("rFrom", help="Search for, with regex uses a regular expression.")
# Arguments with values
cmdParser.add_argument("-r", "--replace", metavar="R", help="Replace with...", default="none")
cmdParser.add_argument("-i", "--input", metavar="I", help="Input file.", default="none")
# True/False arguments
cmdParser.add_argument("-e", "--regex", help="Use Python regular expression to search for text.", action="store_true")
cmdParser.add_argument("-l", "--line", help="Preform operations on whole lines.", action="store_true")
cmdParser.add_argument("-p", "--pipe", help="Take data from Pipe.", action="store_true")
cmdParser.add_argument("-w", "--write", help="Write data to input file.", action="store_true")
# Parse the arguments
args = cmdParser.parse_args()

# Check for input.
if not args.pipe and args.input == "none":
  print("You must have an input!")
  sys.exit(256)
elif args.replace == "none":
  print("You must have an operation for your found text, please use replace.")
  sys.exit(135)
# If there is one an input
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
  print("\n".join(parseLines(lines, args.rFrom, args.replace, args.regex, args.line, True)))
else:
  f.writelines(parseLines(lines, args.rFrom, args.replace, args.regex, args.line))
