
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: wxpTag.py,v 1.1.2.2 2003/06/11 23:54:33 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.lib import wxpTag
_rename(globals(), wxpTag.__dict__, modulename='lib.wxpTag')
del wxpTag
del _rename
