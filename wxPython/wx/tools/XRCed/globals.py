
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: globals.py,v 1.1.2.1 2003/06/11 23:54:25 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython.tools.XRCed import globals
_rename(globals(), globals.__dict__, modulename='tools.XRCed.globals')
del globals
del _rename
