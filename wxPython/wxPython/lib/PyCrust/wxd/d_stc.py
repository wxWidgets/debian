"""Decorator utility for documentation and shell scripting.

When you import stc from this module, all of the classes get decorated
with docstrings from our decoration class definitions.
"""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: d_stc.py,v 1.1.2.1 2003/03/11 19:37:11 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]

from wxPython import stc

import stc_

import decorator

decorator.decorate(real=stc, decoration=stc_)
