import sys
import os
import fileinput
import shelve
import pyflakes.checker

import_db_fname = os.path.join(os.path.expanduser('~'), '.mr.igor')

PRINT = False

def add_missing_imports(checker):
    imports = set()
    for msg in checker.messages:
        if isinstance(msg, pyflakes.messages.UndefinedName):
            name = msg.message_args[0]
            imp = find_import(checker._igor_import_db, name)
            if imp is not None and imp not in imports:
                imports.add(imp)
    if PRINT:
        if len(imports):
            sys.stdout.write("\n".join(imports) + "\n")
        for line in fileinput.input(checker.filename):
            sys.stdout.write(line)
        # avoid the normal pyflakes warnings
        sys.exit()
    else:
        # rewrite file inline
        for i, line in enumerate(fileinput.input(checker.filename, inplace = 1)):
            if i == 0 and len(imports):
                sys.stdout.write("\n".join(imports) + "\n")
            sys.stdout.write(line)

def record_import(db, node):
    source = node.modname
    for (name, alias) in node.names:
        if alias is not None:
            continue
        
        source_counts = db.setdefault(name, {})
        source_counts.setdefault(source, 0)
        source_counts[source] += 1
        db[name] = source_counts
        #print "Recording import. Source: %s. Name: %s" % (source, name)

def find_import(db, name):
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

orig_checker_init = pyflakes.checker.Checker.__init__
def patched_checker_init(self, tree, filename):
    self._igor_import_db = shelve.open(import_db_fname)
    orig_checker_init(self, tree, filename)
    add_missing_imports(self)
pyflakes.checker.Checker.__init__ = patched_checker_init

def patched_checker_del(self):
    self._igor_import_db.close()
pyflakes.checker.Checker.__del__ = patched_checker_del

orig_FROM = pyflakes.checker.Checker.FROM
def patched_FROM(self, node):
    orig_FROM(self, node)
    record_import(self._igor_import_db, node)
pyflakes.checker.Checker.FROM = patched_FROM
