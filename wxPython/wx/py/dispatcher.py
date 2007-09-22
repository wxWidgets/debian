
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: dispatcher.py,v 1.1.2.1 2003/06/11 23:54:28 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython.py import dispatcher
_rename(globals(), dispatcher.__dict__, modulename='py.dispatcher')
del dispatcher
del _rename
