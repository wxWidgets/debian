
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: undo.py,v 1.1.2.1 2003/06/11 23:54:24 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython.tools.XRCed import undo
_rename(globals(), undo.__dict__, modulename='tools.XRCed.undo')
del undo
del _rename
