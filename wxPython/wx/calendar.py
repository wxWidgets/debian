
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: calendar.py,v 1.1.2.2 2003/06/11 23:54:36 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython import calendar
_rename(globals(), calendar.__dict__, modulename='calendar')
del calendar
del _rename
