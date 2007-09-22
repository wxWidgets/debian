"""Decorator classes for documentation and shell scripting.
"""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: Process.py,v 1.1.2.1 2003/04/09 17:43:17 RD Exp $"
__revision__ = "$Revision: 1.1.2.1 $"[11:-2]


# These are not the real wxPython classes. These are Python versions
# for documentation purposes. They are also used to apply docstrings
# to the real wxPython classes, which are SWIG-generated wrappers for
# C-language classes.


from Base import EvtHandler


class Process(EvtHandler):
    """"""

    def CloseOutput(self):
        """"""
        pass

    def Destroy(self):
        """"""
        pass

    def Detach(self):
        """"""
        pass

    def GetErrorStream(self):
        """"""
        pass

    def GetInputStream(self):
        """"""
        pass

    def GetOutputStream(self):
        """"""
        pass

    def IsErrorAvailable(self):
        """"""
        pass

    def IsInputAvailable(self):
        """"""
        pass

    def IsInputOpened(self):
        """"""
        pass

    def IsRedirected(self):
        """"""
        pass

    def Redirect(self):
        """"""
        pass

    def __init__(self):
        """"""
        pass

    def _setCallbackInfo(self):
        """"""
        pass

    def base_OnTerminate(self):
        """"""
        pass

