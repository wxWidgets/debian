
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: stc.py,v 1.1.2.2 2003/06/11 23:54:36 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython import stc
_rename(globals(), stc.__dict__, modulename='stc')
del stc
del _rename
