
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: scrolledpanel.py,v 1.1.2.2 2003/06/11 23:54:33 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.lib import scrolledpanel
_rename(globals(), scrolledpanel.__dict__, modulename='lib.scrolledpanel')
del scrolledpanel
del _rename
