
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: img2py.py,v 1.1.2.1 2003/06/11 23:54:26 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython.tools import img2py
_rename(globals(), img2py.__dict__, modulename='tools.img2py')
del img2py
del _rename
