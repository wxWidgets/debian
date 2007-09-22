"""PyFilling is a python namespace inspection application."""

__author__ = "Patrick K. O'Brien <pobrien@orbtech.com>"
__cvsid__ = "$Id: PyFilling.py,v 1.1.2.3 2003/05/03 16:01:40 PKO Exp $"
__revision__ = "$Revision: 1.1.2.3 $"[11:-2]

# We use this object to get more introspection when run standalone.
app = None

import filling

# These are imported just to have something interesting to inspect.
import crust
import interpreter
import introspect
import pseudo
import shell
import sys
import wx

try:
    True
except NameError:
    True = 1==1
    False = 1==0


class App(filling.App):
    def OnInit(self):
        filling.App.OnInit(self)
        self.root = self.fillingFrame.filling.tree.root
        return True

def main():
    """Create and run the application."""
    global app
    app = App(0)
    app.fillingFrame.filling.tree.Expand(app.root)
    app.MainLoop()


if __name__ == '__main__':
    main()