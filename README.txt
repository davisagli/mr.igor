Mr. Igor provides the parts you need to build your Frankenprogram.

  But how does it know?
    "It'th a knack."

mr.igor is an extension to pyflakes that will learn where you import
things from, and then automatically fill in missing imports from the
place they are most often imported.

Usage: igor [--print] filename

This script will record all imports from filename in Igor's database,
and then add imports at the top of the file for any names that were not
imported but were found in the database.

If the --print option is specified then the rewritten file will be
written to stdout. (This allows the use of igor as a filter for editors.)
Otherwise the file will be modified inplace.

Only "from x import y" style imports are tracked and inserted.  Aliases
("from x import y as z") are not supported.

For now mr.igor stores its import database within the mr.igor egg,
so imports are tracked separately for each Python installation. Note
that this means your mr.igor egg must be writable by the user you are
running the igor script as.
