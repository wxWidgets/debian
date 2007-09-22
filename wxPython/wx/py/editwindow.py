
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: editwindow.py,v 1.1.2.1 2003/06/11 23:54:28 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython.py import editwindow
_rename(globals(), editwindow.__dict__, modulename='py.editwindow')
del editwindow
del _rename
