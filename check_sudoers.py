#!/usr/bin/env python3
"""Usage: check_sudoers.py [--file FILE] [--quiet | --verbose ] [--output FILE]

-h --help               show this
-f FILE --file=FILE     specifiy input file [default: /etc/sudoers]
--quiet                 suppress output
--verbose               print results to stdout
-o FILE --output=FILE   output results to FILE
                        [default: ./check_sudoers_results.out]

"""

import re

from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__)

def get_file(filename):
    """
    Reads a file into a list while removing comments and blank lines,
    and trim leading and trailing whitespace.

    :param filename:
    :return list of lines from the file:
    """

    file = []
    with open(filename) as x:
        for line in x:
            line = line.strip()
            if line.startswith('#'):
                continue
            if not line:
                continue
            if file and file[-1].endswith("\\"):
                file[-1] = file[-1][:-1] + " " + line
            else:
                file.append(line)

    return(file)

def basic_checks(sudoers_file):
    """Perform basic sudoers file security checks.

    Examples: All=(ALL) NOPASSWD: ALL'

    :param sudoers_file
    :return:
    """
    for line in range(len(sudoers_file)):
        # check for (ALL)=ALL errors
        match = re.search(r'all *= *\(all\) .ALL', sudoers_file[line],
                          re.IGNORECASE)
        if match:
            print("The line: ",sudoers_file[line]," possibly contains")
            print("a vunlerability.")
            print("Vulnerability: ALL=(ALL) ALL found. This allows the")
            print("designated user or group to execute any command on the")
            print("system as root.")
            print()

        # check for (ALL)=ALL NOPASSWD errors
        match = re.search(r'NOPASSWD: *ALL', sudoers_file[line], re.IGNORECASE)
        if match:
            print("The line:",sudoers_file[line], "possibly contains a")
            print("vunlerability.")
            print("Vunlerability: 'NOPASSWD: ALL found'. This allows the")
            print("designated user to execute any command without providing")
            print("credentials.")
            print()

def parse_commands(sudoers_file):
    """
    Parse the sudoers file for all commands.

    :param sudoers_file:
    :return:
    """
    for line in range(len(sudoers_file)):
        cur_line = sudoers_file[line]
        #print(cur_line)
        if cur_line.startswith('Host'):
            continue
        if cur_line.startswith('Runas'):
            continue
        if cur_line.startswith('Defaults'):
            continue
        if cur_line.startswith('Cmnd'):
            print(cur_line)
            seperator_index = cur_line.find('=') + 1
            commands = cur_line[seperator_index:-1].split(',')
            commands = [c.strip() for c in commands]
            print(commands)

try:
    sudoers_file = get_file(arguments['--file'])
except IOError:
    print("The file does not exist or is not readable by the current user.")
    quit()

basic_checks(sudoers_file)

parse_commands(sudoers_file)
