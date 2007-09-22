
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: ErrorDialogs_wdr.py,v 1.1.2.1 2003/06/11 23:54:34 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython.lib import ErrorDialogs_wdr
_rename(globals(), ErrorDialogs_wdr.__dict__, modulename='lib.ErrorDialogs_wdr')
del ErrorDialogs_wdr
del _rename
