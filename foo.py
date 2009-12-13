#!/opt/local/bin/python2.6
import sys
sys.path.append('/Users/davidg/ONENW/mr.igor')
import mr.igor
from pyflakes.scripts.pyflakes import checkPath
checkPath('/Users/davidg/ONENW/mr.igor/bar.py')
