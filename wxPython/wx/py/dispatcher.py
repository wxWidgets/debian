
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

from wx import _rename
from wxPython.py import dispatcher
_rename(globals(), dispatcher.__dict__, modulename='py.dispatcher')
del dispatcher
del _rename