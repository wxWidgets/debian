###############################################################################
# Name: __ini__.py                                                            #
# Purpose: CodeBrowser Plugin                                                 #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

# Plugin Meta
"""Adds a CodeBrowser Sidepanel"""
__author__ = "Cody Precord"
__version__ = "0.8"

#-----------------------------------------------------------------------------#
# Imports
import wx
import wx.aui

# Editra Libraries
import iface
import plugin
from profiler import Profile_Get, Profile_Set

# Local imports
import cbrowser

#-----------------------------------------------------------------------------#
# Globals
_ = wx.GetTranslation

#-----------------------------------------------------------------------------#
# Interface implementation
class CodeBrowser(plugin.Plugin):
    """Adds a CodeBrowser to the view menu"""
    plugin.Implements(iface.MainWindowI)

    def PlugIt(self, parent):
        """Adds the view menu entry and registers the event handler"""
        self._mw = parent
        self._log = wx.GetApp().GetLog()
        if self._mw != None:
            self._log("[codebrowser][info] Installing codebrowser plugin")
            
            #---- Create File Browser ----#
            self._codebrowser = cbrowser.CodeBrowserTree(self._mw)
            mgr = self._mw.GetFrameManager()
            mgr.AddPane(self._codebrowser, 
                        wx.aui.AuiPaneInfo().Name(cbrowser.PANE_NAME).\
                            Caption(_("CodeBrowser")).\
                            Top().Right().Layer(0).\
                            CloseButton(True).MaximizeButton(True).\
                            BestSize(wx.Size(215, 350)))
            mgr.Update()

    def GetMenuHandlers(self):
        """Pass even handler for menu item to main window for management"""
        return [(cbrowser.ID_CODEBROWSER, self._codebrowser.OnShowBrowser)]

    def GetMinVersion(self):
        """Get the minimum version of Editra that this plugin is compatible
        with.
        @note: overridden from Plugin

        """
        return "0.3.15"

    def GetUIHandlers(self):
        """Pass Ui handlers to main window for management"""
        return [(cbrowser.ID_CODEBROWSER, self._codebrowser.OnUpdateMenu)]
