import os
import shelve
from pyflakes.checker import Checker

IMPORT_DB_FNAME = os.path.join(os.path.expanduser('~'), '.mr.igor')

class ImportChecker(Checker):
    """ Subclass of the checker from pyflakes that knows how to keep track of
        "from" imports in an external database.
    """

    def __init__(self, tree, filename):
        self._igor_import_db = shelve.open(IMPORT_DB_FNAME)
        super(ImportChecker, self).__init__(tree, filename)
    
    def __del__(self):
        self._igor_import_db.close()
    
    def IMPORTFROM(self, node):
        super(ImportChecker, self).IMPORTFROM(node)

        for alias in node.names:
            if alias.asname is not None:
                continue
            self.record_import(alias.name, node.module)

    def record_import(self, name, source):
        db = self._igor_import_db
        source_counts = db.setdefault(name, {})
        source_counts.setdefault(source, 0)
        source_counts[source] += 1
        db[name] = source_counts

    def find_import(self, name):
        db = self._igor_import_db
        if name in db:
            # find key with max value.
            # in py2.5+ we could use max(db[name], key=db[name].get)
            max = 0
            max_source = None
            for source, count in db[name].iteritems():
                if count > max:
                    max = count
                    max_source = source
            #print "Found import. Source: %s. Name: %s" % (max_source, name)
            return "from %s import %s" % (max_source, name)
