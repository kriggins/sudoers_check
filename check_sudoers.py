#!/usr/bin/env python3
"""Usage: check_sudoers.py [--file FILE] [--quiet | --verbose ] [--output FILE]

-h --help               show this
-f FILE --file=FILE     specifiy input file [default: /etc/sudoers]
--quiet                 suppress output
--verbose               print results to stdout
-o FILE --output=FILE   output results to FILE [default: ./check_sudoers_resutls.out]

"""

import sys
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)
