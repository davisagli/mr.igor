# (mr.igor has already patched pyflakes by virtue of mr.igor
# having been imported)
import sys
from pyflakes.scripts import pyflakes
import mr.igor
def main():
    if sys.argv[1:2] == ['--print']:
        sys.argv = sys.argv[0:1] + sys.argv[2:]
        mr.igor.PRINT = True
    pyflakes.main()
