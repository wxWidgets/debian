
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: ClickableHtmlWindow.py,v 1.1.2.2 2003/06/11 23:54:34 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.lib import ClickableHtmlWindow
_rename(globals(), ClickableHtmlWindow.__dict__, modulename='lib.ClickableHtmlWindow')
del ClickableHtmlWindow
del _rename
