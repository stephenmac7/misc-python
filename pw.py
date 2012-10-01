#!/usr/bin/env python3
# pw: A password manager for the linux cli written in python.
# No encryption at the moment
import os
import sys

# Global constants
TR='\033[0m'       # Text Reset

# Regular Colors
Black='\033[0;30m'        # Black
Red='\033[0;31m'          # Red
Green='\033[0;32m'        # Green
Yellow='\033[0;33m'       # Yellow
Blue='\033[0;34m'         # Blue
Purple='\033[0;35m'       # Purple
Cyan='\033[0;36m'         # Cyan
White='\033[0;37m'        # White

def get_dict():
    """Gets the password dictionary from ~/.pwman"""
    # Open file and get contents
    try:
        open_file = open(os.getenv('HOME') + '/.pwman', 'r')
    except IOError:
        open(os.getenv('HOME') + '/.pwman', 'a').close()
        open_file = open(os.getenv('HOME') + '/.pwman', 'r')
    file_lines = open_file.readlines()
    open_file.close()
    # Create dictionary
    pw_dict = {}
    for pw_pair in [i.replace("\n", "").split(":") for i in file_lines]:
        pw_dict[pw_pair[0]] = [pw_pair[1], pw_pair[2]]
    # Return dictionary
    return pw_dict

def write_dict(pw_dict):
    """Writes the password dictionary to ~/.pwman"""
    # Turn dictionary into writable string list
    w_list = []
    for key in pw_dict.keys():
        w_list.append(key + ':' + pw_dict[key][0] + ':' + pw_dict[key][1])
    # Write passwords to file
    to_write = [i + "\n" for i in w_list]
    open_file = open(os.getenv('HOME') + '/.pwman', 'w')
    open_file.writelines(to_write)
    open_file.close()

def print_pair(pw_dict, key):
    """Prints a username/password pair in a readable way"""
    print("Name:", White + key + TR,
          "Username:", Green + pw_dict[key][0] + TR,
          "Password:", Red + pw_dict[key][1] + TR)

def print_dict(pw_dict):
    """Prints the whole password dictionary."""
    # Add eleven to account for color
    mln = len(max(pw_dict.keys(), key=len)) + 11
    mlu = len(max([pw_dict[i][0] for i in pw_dict.keys()], key=len)) + 11
    mlp = len(max([pw_dict[i][1] for i in pw_dict.keys()], key=len)) + 11
    total = mln + mlu + mlp - 22
    print('{0:{1}} {2:{3}} {4:{5}}'.format(
          (White + "Name" + TR), mln,
          (Green + "Username" + TR), mlu,
          (Red + "Password" + TR), mlp))
    print(total * "-")
    for key in pw_dict.keys():
        print('{0:{1}} {2:{3}} {4:{5}}'.format(
              (White + key + TR), mln,
              (Green + pw_dict[key][0] + TR), mlu,
              (Red + pw_dict[key][1] + TR), mlp))

def search_dict(pw_dict, search_term):
    """Searches and returns list of possible service names."""
    possible_keys = []
    for key in pw_dict.keys():
        if search_term.lower() in key.lower():
            possible_keys.append(key)
    return possible_keys 

def display_help():
    """Display the help"""
    print("""
Options:
-a  | --add          Add a username/password pair
  usage: pw -a name username password
-c  | --clear        Clear all username/password information
  usage: pw -c
-d  | --display      Display a username/password pair
  usage: pw -d name
-f  | --display-full Display all the username/password pairs
  usage: pw -f
-h  | --help         Display this help
  usage: pw -h
-r  | --remove       Remove a username/password pair
  usage: pw -r name
-s  | --search       Search for a name in the db
  usage: pw -s terms

Some commands may be combined to get new results such as search
and display using the format: -sd, not -s -d

NOTE: Refrain from using colons in your names/usernames/passwords
""")

def main():
    """Main function"""
    # Open file, get dictionary
    pw_dict = get_dict()
    # Get and assign operation argument
    try:
        args = sys.argv[1:]
        opr = args[0]
    except IndexError:
        display_help()
        sys.exit(256)
    # If...
    # User wants to add username/password pair
    if opr == '-a' or opr == '--add':
        pw_dict[args[1]] = [args[2], args[3]]
    # User wants to clear everything
    if opr == '-c' or opr == '--clear':
        confirm = input(Red + "Are you sure you want to clear all your usernames/passwords? " + TR)
        if confirm.lower() == 'y' or confirm.lower() == 'yes':
            pw_dict = {}
    # User wants to display username/password pair
    elif opr == '-d' or opr == '--display':
        print_pair(pw_dict, args[1])
    # User wants to display full dictionary
    elif opr == '-f' or opr == '--display-full':
        print_dict(pw_dict)
    # User wants to get help
    elif opr == '-h' or opr == '--help':
        display_help()
    # User wants to remove a username/password pair
    elif opr == '-r' or opr == '--remove':
        pw_dict.pop(args[1])
    # User wants to search for a name
    elif opr == '-s' or opr == '--search':
        [print(i) for i in search_dict(pw_dict, args[1])]
    # User want to search for and a display a username/password pair
    elif opr == '-sd' or opr == '--search-and-display':
        new_dict = {}
        for i in search_dict(pw_dict, args[1]):
            new_dict[i] = pw_dict[i]
        print_dict(new_dict)
    # Save the new, modified dictionary (Even though there may have been no changes)
    write_dict(pw_dict)

main()
