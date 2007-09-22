
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: rightalign.py,v 1.1.2.2 2003/06/11 23:54:33 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.lib import rightalign
_rename(globals(), rightalign.__dict__, modulename='lib.rightalign')
del rightalign
del _rename
