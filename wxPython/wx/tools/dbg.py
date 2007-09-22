
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: dbg.py,v 1.1.2.1 2003/06/11 23:54:26 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython.tools import dbg
_rename(globals(), dbg.__dict__, modulename='tools.dbg')
del dbg
del _rename
