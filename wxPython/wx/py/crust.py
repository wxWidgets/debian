
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: crust.py,v 1.1.2.1 2003/06/11 23:54:28 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython.py import crust
_rename(globals(), crust.__dict__, modulename='py.crust')
del crust
del _rename
