import os
import sys
import tempfile
import unittest
from StringIO import StringIO

from mr.igor import main as igor

class TestIgor(unittest.TestCase):
    """ Functional test for Igor. """

    def setUp(self):
        (fd, self.filename) = tempfile.mkstemp(text=True)
        os.close(fd)
        
        # Populate db
        f = open(self.filename, 'w')
        f.write('from foo import bar, baz')
        f.close()
        igor(self.filename)
        
        # Now manually remove the import
        f = open(self.filename, 'w')
        f.write('bar\nbaz')
        f.close()
        
        self.expected = "from foo import bar\nfrom foo import baz\nbar\nbaz"

    def testIgorPrinted(self):
        hold_stdout = sys.stdout
        sys.stdout = out = StringIO()
        igor('--print', self.filename)
        sys.stdout = hold_stdout
        self.assertEqual(out.getvalue(), self.expected)
        # make sure the file wasn't touched
        self.assertEqual(open(self.filename).read(), "bar\nbaz")

    def testIgorInplace(self):
        # Now run Igor in normal mode and make sure the import was replaced.
        igor(self.filename)
        self.assertEqual(open(self.filename).read(), self.expected)

    def tearDown(self):
        os.unlink(self.filename)

if __name__ == '__main__':
    unittest.main()
