Mr. Igor provides the parts you need to build your Frankenprogram.

  But how does it know?
    "It'th a knack."

mr.igor is an extension to pyflakes that will learn where you import
things from, and then automatically fill in missing imports from the
place they are most often imported.

Only "from x import y" style imports are tracked and inserted.  Aliases
("from x import y as z") are not supported.

mr.igor installs itself by monkeypatching pyflakes, so in order to
use it you must modify your pyflakes script to import mr.igor before
it runs the main pyflakes function, like this::

  #!/opt/local/bin/python2.6
  import mr.igor
  from pyflakes.scripts.pyflakes import main
  main()

For now mr.igor stores its import database within the mr.igor egg,
so imports are tracked separately for each Python installation. Note
that this means your mr.igor egg must be writable by the user you are
running pyflakes as.
