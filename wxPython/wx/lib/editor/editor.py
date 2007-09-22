
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: editor.py,v 1.1.2.2 2003/06/11 23:54:31 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.lib.editor import editor
_rename(globals(), editor.__dict__, modulename='lib.editor.editor')
del editor
del _rename
