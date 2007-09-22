
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: PyAlaMode.py,v 1.1.2.2 2003/06/11 23:54:28 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.py import PyAlaMode
_rename(globals(), PyAlaMode.__dict__, modulename='py.PyAlaMode')
del PyAlaMode
del _rename
