
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: buttons.py,v 1.1.2.2 2003/06/11 23:54:34 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.lib import buttons
_rename(globals(), buttons.__dict__, modulename='lib.buttons')
del buttons
del _rename
