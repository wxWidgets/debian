
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: panel.py,v 1.1.2.1 2003/06/11 23:54:25 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wx import _rename
from wxPython.tools.XRCed import panel
_rename(globals(), panel.__dict__, modulename='tools.XRCed.panel')
del panel
del _rename
