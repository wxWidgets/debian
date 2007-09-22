
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: shell.py,v 1.1.2.1 2003/06/11 23:54:28 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython.py import shell
_rename(globals(), shell.__dict__, modulename='py.shell')
del shell
del _rename
