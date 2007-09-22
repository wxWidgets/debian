"""Decorator classes for documentation and shell scripting.
"""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: Accelerators.py,v 1.1.2.1 2003/04/09 17:43:21 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]


# These are not the real wxPython classes. These are Python versions
# for documentation purposes. They are also used to apply docstrings
# to the real wxPython classes, which are SWIG-generated wrappers for
# C-language classes.


from Base import Object
import Parameters as wx


class AcceleratorEntry:
    """"""

    def __init__(self):
        """"""
        pass

    def __del__(self):
        """"""
        pass

    def GetCommand(self):
        """"""
        pass

    def GetFlags(self):
        """"""
        pass

    def GetKeyCode(self):
        """"""
        pass

    def Set(self):
        """"""
        pass


class AcceleratorTable(Object):
    """"""

    def __init__(self):
        """"""
        pass

    def __del__(self):
        """"""
        pass

