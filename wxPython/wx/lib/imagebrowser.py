
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: imagebrowser.py,v 1.1.2.2 2003/06/11 23:54:33 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.lib import imagebrowser
_rename(globals(), imagebrowser.__dict__, modulename='lib.imagebrowser')
del imagebrowser
del _rename
