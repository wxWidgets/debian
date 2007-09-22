
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: encode_bitmaps.py,v 1.1.2.1 2003/06/11 23:54:25 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython.tools.XRCed import encode_bitmaps
_rename(globals(), encode_bitmaps.__dict__, modulename='tools.XRCed.encode_bitmaps')
del encode_bitmaps
del _rename
