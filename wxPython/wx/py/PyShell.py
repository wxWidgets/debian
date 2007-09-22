
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: PyShell.py,v 1.1.2.2 2003/06/11 23:54:28 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.py import PyShell
_rename(globals(), PyShell.__dict__, modulename='py.PyShell')
del PyShell
del _rename
