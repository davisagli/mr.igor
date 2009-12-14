# (mr.igor has already patched pyflakes by virtue of mr.igor
# having been imported)
import sys
from pyflakes.scripts import pyflakes
import mr.igor
def main():
    if len(sys.argv) == 1 or sys.argv[1:2] in (['-h'], ['--help']):
        print """
Igor records your imports and adds missing imports for names it recognizes.
Usage: igor [--print] filename

  --print  Causes Igor to write the modified file to stdout rather than
           making changes inplace.
"""
    else:    
        if sys.argv[1:2] == ['--print']:
            sys.argv = sys.argv[0:1] + sys.argv[2:3]
            mr.igor.PRINT = True
        pyflakes.main()
