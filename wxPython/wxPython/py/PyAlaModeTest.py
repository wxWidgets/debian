"""PyAlaModeTest is a programmer's editor."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: PyAlaModeTest.py,v 1.1.2.3 2003/05/03 16:01:41 PKO Exp $"
__revision__ = "$Revision: 1.1.2.3 $"[11:-2]

import wx

import os
import sys

import editor

try:
    True
except NameError:
    True = 1==1
    False = 1==0

class App(wx.App):
    """PyAlaModeTest standalone application."""

    def __init__(self, filename=None):
        self.filename = filename
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        wx.InitAllImageHandlers()
        self.frame = editor.EditorShellNotebookFrame(filename=self.filename)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def main(filename=None):
    app = App(filename)
    app.MainLoop()

if __name__ == '__main__':
    filename = None
    if len(sys.argv) > 1:
        filename = os.path.realpath(sys.argv[1])
    main(filename)
