
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: floatbar.py,v 1.1.2.2 2003/06/11 23:54:33 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.lib import floatbar
_rename(globals(), floatbar.__dict__, modulename='lib.floatbar')
del floatbar
del _rename
