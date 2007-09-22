
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: rubberband.py,v 1.1.2.2 2003/06/11 23:54:30 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.lib.mixins import rubberband
_rename(globals(), rubberband.__dict__, modulename='lib.mixins.rubberband')
del rubberband
del _rename
