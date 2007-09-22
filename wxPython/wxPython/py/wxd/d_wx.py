"""Decorator utility for documentation and shell scripting.

When you import wx from this module, all of the classes get decorated
with docstrings from our decoration class definitions.
"""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: d_wx.py,v 1.1.2.1 2003/04/09 17:43:16 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wxPython import wx

import wx_

import decorator

decorator.decorate(real=wx, decoration=wx_)
