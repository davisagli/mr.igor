import os
import sys
import shelve
import shutil
import tempfile
import unittest
from StringIO import StringIO

from mr.igor import main as igor
from mr.igor import checker

# shelve may use a physical filename other than the base filename (e.g.
# mr.igor.db). So we can forcibly delete it, create the file inside a
# trashable directory with a guaranteed name.
checker.IMPORT_DB_BASE_FILENAME += '.test.d/mr.igor'
TEST_DB_DIRNAME = checker.IMPORT_DB_BASE_FILENAME[:-len('/mr.igor')]

class TestIgor(unittest.TestCase):
    """ Functional test for Igor. """

    def setUp(self):
        if os.path.exists(TEST_DB_DIRNAME):
            shutil.rmtree(TEST_DB_DIRNAME)
        os.mkdir(TEST_DB_DIRNAME)

        (fd, self.filename) = tempfile.mkstemp(text=True)
        os.close(fd)

        # Populate db
        f = open(self.filename, 'w')
        f.write('from foo import bar, baz')
        f.close()
        igor(self.filename)

        # Now manually remove the import
        f = open(self.filename, 'w')
        f.write('bar\nbaz\n')
        f.close()

        self.expected = "from foo import bar\nfrom foo import baz\nbar\nbaz\n"

    def testIgorPrinted(self):
        hold_stdout = sys.stdout
        sys.stdout = out = StringIO()
        igor('--print', self.filename)
        sys.stdout = hold_stdout
        self.assertEqual(out.getvalue(), self.expected)
        # make sure the file wasn't touched
        self.assertEqual(open(self.filename).read(), "bar\nbaz\n")

    def testIgorInplace(self):
        # Now run Igor in normal mode and make sure the import was replaced.
        igor(self.filename)
        f = open(self.filename)
        self.assertEqual(f.read(), self.expected)
        f.close()

    def testIgorPrintsOriginalIfNoImportsFound(self):
        # make sure the original file is still output in print mode
        # if Igor found no new imports
        f = open(self.filename, 'w')
        f.write('qux')
        f.close()

        hold_stdout = sys.stdout
        sys.stdout = out = StringIO()
        igor('--print', self.filename)
        sys.stdout = hold_stdout
        self.assertEqual(out.getvalue(), 'qux')

    def testPrintModeDoesNothingOnSyntaxError(self):
        f = open(self.filename, 'w')
        f.write('from')
        f.close()

        hold_stdout = sys.stdout
        sys.stdout = out = StringIO()
        igor('--print', self.filename)
        sys.stdout = hold_stdout
        self.assertEqual(out.getvalue(), 'from')

    def testIgorReapMode(self):
        # make sure test db starts empty
        if os.path.exists(TEST_DB_DIRNAME):
            shutil.rmtree(TEST_DB_DIRNAME)
        os.mkdir(TEST_DB_DIRNAME)

        f = open(self.filename, 'w')
        f.write('from foo import bar, baz')
        f.close()

        hold_stdout = sys.stdout
        sys.stdout = out = StringIO()
        igor('--reap', self.filename)
        sys.stdout = hold_stdout

        self.failIf(out.getvalue())
        self.failUnless(len(shelve.open(checker.IMPORT_DB_BASE_FILENAME)))

    def testInitialSimpleComments(self):
        f = open(self.filename, 'w')
        f.write('# -*- coding: utf8 -*-\nbar\nbaz\n')
        f.close()

        expected = "# -*- coding: utf8 -*-\nfrom foo import bar\nfrom foo import baz\nbar\nbaz\n"

        igor(self.filename)
        f = open(self.filename)
        self.assertEqual(f.read(), expected)
        f.close()


    def tearDown(self):
        shutil.rmtree(TEST_DB_DIRNAME)
        os.unlink(self.filename)

if __name__ == '__main__':
    unittest.main()
