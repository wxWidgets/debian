
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

from wx import _rename
from wxPython.tools.XRCed import tools
_rename(globals(), tools.__dict__, modulename='tools.XRCed.tools')
del tools
del _rename