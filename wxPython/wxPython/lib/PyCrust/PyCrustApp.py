"""PyCrustApp is a python shell and namespace browser application."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: PyCrustApp.py,v 1.9.2.2 2002/12/16 18:19:42 RD Exp $"
__revision__ = "$Revision: 1.9.2.2 $"[11:-2]

from wxPython import wx
from crust import CrustFrame

True, False = 1, 0


class App(wx.wxApp):
    """PyCrust standalone application."""

    def OnInit(self):
        wx.wxInitAllImageHandlers()
        locals = {'__app__': 'PyCrust Standalone Application'}
        self.crustFrame = CrustFrame(locals=locals)
        self.crustFrame.SetSize((750, 525))
        self.crustFrame.Show(True)
        self.SetTopWindow(self.crustFrame)
        # Add the application object to the sys module's namespace.
        # This allows a shell user to do:
        # >>> import sys
        # >>> sys.application.whatever
        import sys
        sys.application = self
        return True


def main():
    application = App(0)
    application.MainLoop()

if __name__ == '__main__':
    main()


