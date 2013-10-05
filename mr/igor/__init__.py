import sys
import os
import fileinput
import pyflakes
import _ast
from mr.igor.checker import ImportChecker

def check(fname, output):
    """ Check a file's imports and output missing imports using the output function. """
    if os.path.exists(fname):
        codestring = file(fname, 'U').read() + '\n'
    else:
        print >> sys.stderr, '%s: no such file' % fname
        return 1
        
    try:
        tree = compile(codestring, fname, "exec", _ast.PyCF_ONLY_AST)
    except (SyntaxError, IndentationError):
        if output is print_output:
            # silently ignore syntax errors in print mode, to avoid clobbering
            # things when we're used as a filter
            output('', fname)
            return
        else:
            value = sys.exc_info()[1]
            try:
                (lineno, offset, line) = value[1][1:]
            except IndexError:
                print >> sys.stderr, 'could not compile %r' % (fname,)
                return 1
            if line.endswith("\n"):
                line = line[:-1]
            print >> sys.stderr, '%s:%d: could not compile' % (fname, lineno)
            print >> sys.stderr, line
            print >> sys.stderr, " " * (offset-2), "^"
    else:
        imports = set()

        with ImportChecker(tree, fname) as checker:
            for msg in checker.messages:
                if isinstance(msg, pyflakes.messages.UndefinedName):
                    name = msg.message_args[0]
                    imp = checker.find_import(name)
                    if imp is not None and imp not in imports:
                        imports.add(imp)

        if imports:
            output("\n".join(imports) + "\n", fname)
        else:
            output('', fname)

def print_output(imports, fname):
    """ Outputs by printing the modified file to stdout. """
    in_initial_comments = True
    for line in fileinput.input(fname):
        if in_initial_comments:
            if not line.startswith('#'):
                in_initial_comments = False
                sys.stdout.write(imports)
        sys.stdout.write(line)

def null_output(imports, fname):
    pass

def edit_inplace(imports, fname):
    """ Outputs by modifying file inplace. """
    # rewrite file inline
    in_initial_comments = True
    for i, line in enumerate(fileinput.input(fname, inplace = 1)):
        if in_initial_comments:
            if not line.startswith('#'):
                in_initial_comments = False
                sys.stdout.write(imports)
        sys.stdout.write(line)

def main(*args):
    args = list(args)
    if not len(args):
        args = sys.argv[1:]
    
    if not len(args) or args[0:1] in (['-h'], ['--help']):
        print_help()
        return 1
    
    if args[0:1] == ['--print']:
        args = args[1:]
        output = print_output
    elif args[0:1] == ['--reap']:
        args = args[1:]
        output = null_output
    else:
        output = edit_inplace
        
    try:
        fname = args[0]
    except IndexError:
        print >> sys.stderr, "Expected filename."
        return 1

    return check(fname, output=output)

def print_help():
    print >> sys.stderr, """
Igor records your imports and adds missing imports for names it recognizes.
Usage: igor [--print] filename

  --print  Causes Igor to write the modified file to stdout rather than
           making changes inplace.
"""
