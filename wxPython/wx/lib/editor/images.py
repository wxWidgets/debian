
"""Renamer stub: provides a way to drop the wx prefix from wxPython objects."""

__cvsid__ = "$Id: images.py,v 1.1.2.2 2003/06/11 23:54:31 RD Exp $"
__revision__ = "$Revision: 1.1.2.2 $"[11:-2]

from wx import _rename
from wxPython.lib.editor import images
_rename(globals(), images.__dict__, modulename='lib.editor.images')
del images
del _rename
