
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

from wx import _rename
from wxPython.lib import sheet
_rename(globals(), sheet.__dict__, modulename='lib.sheet')
del sheet
del _rename