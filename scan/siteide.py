import sys

from robotide import main
import Selenium2Library

# Must be protected against reimporting
# As multiprocessing has an odd requirement
# and we use multiprocessing
# http://docs.python.org/library/multiprocessing.html#windows
if __name__ == '__main__':
    main(*sys.argv[1:])