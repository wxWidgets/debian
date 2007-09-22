
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: PyCrust.py,v 1.1.2.2 2003/06/11 23:54:28 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.py import PyCrust
_rename(globals(), PyCrust.__dict__, modulename='py.PyCrust')
del PyCrust
del _rename
