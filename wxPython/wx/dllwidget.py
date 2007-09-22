
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: dllwidget.py,v 1.1.2.1 2003/06/11 23:54:36 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython import dllwidget
_rename(globals(), dllwidget.__dict__, modulename='dllwidget')
del dllwidget
del _rename
