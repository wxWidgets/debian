
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: iewin.py,v 1.1.2.2 2003/06/11 23:56:55 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython import iewin
_rename(globals(), iewin.__dict__, modulename='iewin')
del iewin
del _rename