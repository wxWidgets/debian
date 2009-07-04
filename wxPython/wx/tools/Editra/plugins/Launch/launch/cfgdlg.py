# -*- coding: utf-8 -*-
###############################################################################
# Name: cfgdlg.py                                                             #
# Purpose: Configuration Dialog                                               #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Launch Configuration Dialog"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: cfgdlg.py 60140 2009-04-14 15:12:34Z CJP $"
__revision__ = "$Revision: 60140 $"

#-----------------------------------------------------------------------------#
# Imports
import sys
import wx
import wx.lib.mixins.listctrl as listmix
import cStringIO
import zlib

# Local Imports
import handlers

# Editra Libraries
import eclib
import util
import ed_msg
from profiler import Profile_Get, Profile_Set

#-----------------------------------------------------------------------------#
# Globals

# Profile Key
LAUNCH_PREFS = 'Launch.Prefs'

# General Panel
ID_LANGUAGE = wx.NewId()
ID_EXECUTABLES = wx.NewId()

# Misc Panel
ID_AUTOCLEAR = wx.NewId()

# Color Buttons
ID_DEF_BACK = wx.NewId()
ID_DEF_FORE = wx.NewId()
ID_INFO_BACK = wx.NewId()
ID_INFO_FORE = wx.NewId()
ID_ERR_BACK = wx.NewId()
ID_ERR_FORE = wx.NewId()
ID_WARN_BACK = wx.NewId()
ID_WARN_FORE = wx.NewId()

COLOR_MAP = { ID_DEF_BACK : 'defaultb', ID_DEF_FORE : 'defaultf',
              ID_ERR_BACK : 'errorb',   ID_ERR_FORE : 'errorf',
              ID_INFO_BACK : 'infob',   ID_INFO_FORE : 'infof',
              ID_WARN_BACK : 'warnb',   ID_WARN_FORE : 'warnf'}

# Message Types
EDMSG_LAUNCH_CFG_EXIT = ed_msg.EDMSG_ALL + ('launch', 'cfg', 'exit')

_ = wx.GetTranslation
#-----------------------------------------------------------------------------#

def GetMinusData():
    return zlib.decompress(
"x\xda\xeb\x0c\xf0s\xe7\xe5\x92\xe2b``\xe0\xf5\xf4p\t\x02\xd2< \xcc\xc1\x06$\
\xc3Jc\x9e\x03)\x96b'\xcf\x10\x0e \xa8\xe1H\xe9\x00\xf2\x9d<]\x1cC4&&\xa7\
\xa4$\xa5)\xb0\x1aL\\RU\x90\x95\xe0\xf8,\xc6\xaa\xf0\xcf\xffr\x13\xd69\x87\
\xb8x\xaaVM\xea\x890\xf512N\x9e\xb1v\xf5\xe9\x05\xdc\xc2;jf:\x96\xdf\xd2\x14\
a\x96pO\xda\xc0\xc4\xa0\xf4\x8a\xab\xcau\xe2|\x1d\xa0i\x0c\x9e\xae~.\xeb\x9c\
\x12\x9a\x00Ij($" )

def GetMinusBitmap():
    stream = cStringIO.StringIO(GetMinusData())
    return wx.BitmapFromImage(wx.ImageFromStream(stream))

#----------------------------------------------------------------------
def GetPlusData():
    return zlib.decompress(
"x\xda\xeb\x0c\xf0s\xe7\xe5\x92\xe2b``\xe0\xf5\xf4p\t\x02\xd2< \xcc\xc1\x06$\
\xc3Jc\x9e\x03)\x96b'\xcf\x10\x0e \xa8\xe1H\xe9\x00\xf2{<]\x1cC4&&'Hp\x1c\
\xd8\xb9\xcf\xe6U\xfd\xefi\xbb\xffo\xf44J\x14L\xae\xde\x97+yx\xd3\xe9\xfc\
\x8d\xb3\xda|\x99\x99g\x1b07\x1b\xd8k\x87\xf1\xea\x18\x1c{\xaa\xec\xfe\xaf>%\
!\xf9A\xda\xef\x03\x06\xf67{\x1f\x1e\xf8\xf9\x98g\xf9\xb9\xf9\xbf\xfe\xbf~\
\xad\xcf\x96'h\xca\xe6\xcck\xe8&2\xb7\x8e\x87\xe7\xbfdAB\xfb\xbf\xe0\x88\xbf\
\xcc\xcc\x7f.\xcbH\xfc{\xfd(\xa0\xe5*\xff\xfd\xff\x06\x06\x1f\xfe\xffh\xbaj\
\xf2f^ZB\xc2\x83\xe4\xc3\xef2o13<r\xd5y\xc0\xb9\xc2\xfa\x0e\xd0]\x0c\x9e\xae\
~.\xeb\x9c\x12\x9a\x00\xcf9S\xc6" )

def GetPlusBitmap():
    stream = cStringIO.StringIO(GetPlusData())
    return wx.BitmapFromImage(wx.ImageFromStream(stream))

#----------------------------------------------------------------------

class ConfigDialog(wx.Frame):
    """Configuration dialog for configuring what executables are available
    for a filetype and what the preferred one is.

    """
    def __init__(self, parent, ftype=0):
        """Create the ConfigDialog
        @param parent: The parent window
        @keyword: The filetype to set

        """
        wx.Frame.__init__(self, parent, title=_("Launch Configuration"))

        # Layout
        util.SetWindowIcon(self)
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        # Register with app
        wx.GetApp().RegisterWindow(repr(self), self)

    def __DoLayout(self):
        """Layout the dialog"""
        sizer = wx.BoxSizer(wx.VERTICAL)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        noteb = ConfigNotebook(panel)
        hsizer.AddMany([((5, 5), 0), (noteb, 1, wx.EXPAND), ((5, 5), 0)])
        vsizer.AddMany([((5, 5), 0), (hsizer, 1, wx.EXPAND), ((10, 10), 0)])
        panel.SetSizer(vsizer)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
        self.SetInitialSize()
        self.SetMinSize((420, 345))

    def OnClose(self, evt):
        """Unregister the window when its closed"""
        wx.GetApp().UnRegisterWindow(repr(self))
        evt.Skip()

#-----------------------------------------------------------------------------#

class ConfigNotebook(wx.Notebook):
    """Notebook for holding config pages"""
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent)

        # Make sure config has been intialized
        prefs = Profile_Get(LAUNCH_PREFS, default=None)
        if prefs is None:
            buff = eclib.OutputBuffer(self)
            buff.Hide()
            Profile_Set(LAUNCH_PREFS,
                        dict(autoclear=False,
                             defaultf=buff.GetDefaultForeground().Get(),
                             defaultb=buff.GetDefaultBackground().Get(),
                             errorf=buff.GetErrorForeground().Get(),
                             errorb=buff.GetErrorBackground().Get(),
                             infof=buff.GetInfoForeground().Get(),
                             infob=buff.GetInfoBackground().Get(),
                             warnf=buff.GetWarningForeground().Get(),
                             warnb=buff.GetWarningBackground().Get()))
            buff.Destroy()

        # Setup
        self.AddPage(ConfigPanel(self), _("General"))
        self.AddPage(MiscPanel(self), _("Misc"))

    def __del__(self):
        ed_msg.PostMessage(EDMSG_LAUNCH_CFG_EXIT)

#-----------------------------------------------------------------------------#

class ConfigPanel(wx.Panel):
    """Configuration panel that holds the controls for configuration"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_CHOICE, self.OnChoice)
        self.Bind(wx.EVT_LIST_END_LABEL_EDIT, self.OnEndEdit)

    def __DoLayout(self):
        """Layout the controls"""
        msizer = wx.BoxSizer(wx.VERTICAL)

        lsizer = wx.BoxSizer(wx.HORIZONTAL)
        ftype = wx.GetApp().GetCurrentBuffer().GetLangId()
        ftype = handlers.GetHandlerById(ftype).GetName()
        htypes = GetHandlerTypes()
        lang_ch = wx.Choice(self, ID_LANGUAGE, choices=htypes)
        if ftype != handlers.DEFAULT_HANDLER:
            lang_ch.SetStringSelection(ftype)
        else:
            lang_ch.SetStringSelection(htypes[0])

        lsizer.AddMany([(wx.StaticText(self, label=_("File Type") + ":"), 0,
                         wx.ALIGN_CENTER_VERTICAL), ((5, 5), 0),
                        (lang_ch, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)])

        # Main area
        sbox = wx.StaticBox(self, label=_("Executables"))
        boxsz = wx.StaticBoxSizer(sbox, wx.VERTICAL)

        # Default exe
        dsizer = wx.BoxSizer(wx.HORIZONTAL)
        chandler = handlers.GetHandlerByName(lang_ch.GetStringSelection())
        cmds = chandler.GetAliases()
        def_ch = wx.Choice(self, wx.ID_DEFAULT, choices=cmds)
        if chandler.GetName() != handlers.DEFAULT_HANDLER:
            def_ch.SetStringSelection(chandler.GetDefault())
        elif len(cmds):
            def_ch.SetStringSelection(cmds[0])
        else:
            pass

        dsizer.AddMany([(wx.StaticText(self, label=_("Default") + ":"), 0,
                         wx.ALIGN_CENTER_VERTICAL), ((5, 5), 0),
                        (def_ch, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL)])

        # Executables List
        exelist = CommandListCtrl(self, ID_EXECUTABLES,
                                  style=wx.LC_EDIT_LABELS|\
                                        wx.BORDER|wx.LC_REPORT|\
                                        wx.LC_SINGLE_SEL)
#        exelist.SetToolTipString(_("Click on an item to edit"))
#        exelist.InsertColumn(0, _("Alias"))
#        exelist.InsertColumn(1, _("Executable Commands"))
        self.SetListItems(chandler.GetCommands())
        addbtn = wx.BitmapButton(self, wx.ID_ADD, GetPlusBitmap())
        addbtn.SetToolTipString(_("Add a new executable"))
        delbtn = wx.BitmapButton(self, wx.ID_REMOVE, GetMinusBitmap())
        delbtn.SetToolTipString(_("Remove selection from list"))
        btnsz = wx.BoxSizer(wx.HORIZONTAL)
        btnsz.AddMany([(addbtn, 0), ((2, 2), 0), (delbtn, 0)])

        # Box Sizer Layout
        boxsz.AddMany([((5, 5), 0), (dsizer, 0, wx.ALIGN_CENTER|wx.EXPAND),
                       ((5, 5), 0), (wx.StaticLine(self), 0, wx.EXPAND),
                       ((8, 8), 0), (exelist, 1, wx.EXPAND), ((5, 5), 0),
                       (btnsz, 0, wx.ALIGN_LEFT)])

        # Setup the main sizer
        msizer.AddMany([((10, 10), 0), (lsizer, 0, wx.EXPAND),
                        ((10, 10), 0), (wx.StaticLine(self), 0, wx.EXPAND),
                        ((10, 10), 0),
                        (boxsz, 1, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL),
                        ((10, 10), 0)])

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddMany([((8, 8), 0), (msizer, 1, wx.EXPAND), ((8, 8), 0)])
        self.SetSizer(hsizer)
        self.SetAutoLayout(True)

    def __DoUpdateHandler(self, handler):
        exes = self.GetListItems()
        handler.SetCommands(exes)
        def_ch = self.FindWindowById(wx.ID_DEFAULT)
        def_ch.SetItems(handler.GetAliases())
        def_ch.SetStringSelection(handler.GetDefault())

    def GetCurrentHandler(self):
        """Get the currently selected file type handler
        @return: handlers.FileTypeHandler

        """
        ftype = self.FindWindowById(ID_LANGUAGE).GetStringSelection()
        return handlers.GetHandlerByName(ftype)

    def GetListItems(self):
        """Get all the values from the list control
        return: tuple (alias, cmd)

        """
        item_id = -1
        exes = list()
        elist = self.FindWindowById(ID_EXECUTABLES)
        for item in xrange(elist.GetItemCount()):
            item_id = elist.GetNextItem(item_id)
            if item_id == -1:
                break
            val = (elist.GetItem(item_id, 0).GetText(),
                   elist.GetItem(item_id, 1).GetText())
            exes.append(val)
        return exes

    def OnButton(self, evt):
        """Handle the add and remove button events
        @param evt: wxButtonEvent

        """
        e_id = evt.GetId()
        elist = self.FindWindowById(ID_EXECUTABLES)
        if e_id == wx.ID_ADD:
            elist.Append([_("**Alias**"), _("**New Value**")])
        elif e_id == wx.ID_REMOVE:
            item = -1
            items = []
            while True:
                item = elist.GetNextItem(item, wx.LIST_NEXT_ALL,
                                         wx.LIST_STATE_SELECTED)
                if item == -1:
                    break
                items.append(item)

            for item in reversed(sorted(items)):
                elist.DeleteItem(item)

            wx.CallAfter(self.__DoUpdateHandler, self.GetCurrentHandler())

        else:
            evt.Skip()

    def OnChoice(self, evt):
        """Handle the choice selection events"""
        e_id = evt.GetId()
        e_obj = evt.GetEventObject()
        e_val = e_obj.GetStringSelection()
        if e_id == ID_LANGUAGE:
            handler = handlers.GetHandlerByName(e_val)
            elist = self.FindWindowById(ID_EXECUTABLES)
            elist.DeleteAllItems()
            def_ch = self.FindWindowById(wx.ID_DEFAULT)
            def_ch.SetItems(handler.GetAliases())
            def_ch.SetStringSelection(handler.GetDefault())
            self.SetListItems(handler.GetCommands())
        elif e_id == wx.ID_DEFAULT:
            handler = self.GetCurrentHandler()
            handler.SetDefault((e_val, handler.GetCommand(e_val)))
        else:
            evt.Skip()

    def OnEndEdit(self, evt):
        """Store the new list values after the editing of a
        label has finished.
        @param evt: wxEVT_LIST_END_LABEL_EDIT
        @note: values in list are set until after this handler has finished

        """
        handler = self.GetCurrentHandler()
        if handler.GetName() != handlers.DEFAULT_HANDLER:
            exes = self.GetListItems()
            idx = evt.GetIndex()
            col = evt.GetColumn()
            nval = evt.GetLabel()
            if len(exes) >= idx:
                # Update an existing item
                if col == 0:
                    exes[idx] = (nval, exes[idx][1])
                else:
                    exes[idx] = (exes[idx][0], nval)
            else:
                # Add a new item
                # This should not happen
                if col == 0:
                    exes.append((nval, nval))
                else:
                    exes.append((nval, nval))

            # Store the new values
            handler.SetCommands(exes)
            def_ch = self.FindWindowById(wx.ID_DEFAULT)
            def_ch.SetItems(handler.GetAliases())
            def_ch.SetStringSelection(handler.GetDefault())

    def SetListItems(self, items):
        """Set the items that are in the list control
        @param items: list of tuples (alias, cmd)

        """
        elist = self.FindWindowById(ID_EXECUTABLES)
        for exe in items:
            elist.Append(exe)

#-----------------------------------------------------------------------------#

class MiscPanel(wx.Panel):
    """Misc settings panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Attributes

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_CHECKBOX, self.OnCheck)
        self.Bind(eclib.EVT_COLORSETTER, self.OnColor)

    def __DoLayout(self):
        """Layout the controls"""
        msizer = wx.BoxSizer(wx.VERTICAL)
        sbox = wx.StaticBox(self, label=_("Text Colors"))
        boxsz = wx.StaticBoxSizer(sbox, wx.VERTICAL)

        # Launch Config
        cfg = Profile_Get(LAUNCH_PREFS, default=dict())

        # Actions Configuration
        clear_cb = wx.CheckBox(self, ID_AUTOCLEAR,
                               _("Automatically clear buffer between runs"))
        clear_cb.SetValue(cfg.get('autoclear', False))

        # Colors
        colors = dict()
        for btn in COLOR_MAP.iteritems():
            cbtn = eclib.ColorSetter(self, btn[0], color=cfg.get(btn[1]))
            colors[btn[0]] = cbtn

        flexg = wx.FlexGridSizer(5, 5, 5, 5)
        flexg.AddGrowableCol(1, 1)
        flexg.AddGrowableCol(3, 1)
        flexg.AddMany([# First Row
                       ((5, 5), 0), ((5, 5), 1),
                       (wx.StaticText(self, label=_("Foreground")), 0,
                        wx.ALIGN_CENTER),
                       ((5, 5), 1),
                       (wx.StaticText(self, label=_("Background")), 0,
                        wx.ALIGN_CENTER),
                       # Second Row
                       (wx.StaticText(self, label=_("Plain Text") + u":"), 0,
                        wx.ALIGN_CENTER_VERTICAL),
                       ((5, 5), 1),
                       (colors[ID_DEF_FORE], 0, wx.EXPAND),
                       ((5, 5), 1),
                       (colors[ID_DEF_BACK], 0, wx.EXPAND),
                       # Third Row
                       (wx.StaticText(self, label=_("Error Text") + u":"), 0,
                        wx.ALIGN_CENTER_VERTICAL),
                       ((5, 5), 1),
                       (colors[ID_ERR_FORE], 0, wx.EXPAND),
                       ((5, 5), 1),
                       (colors[ID_ERR_BACK], 0, wx.EXPAND),
                       # Fourth Row
                       (wx.StaticText(self, label=_("Info Text") + u":"), 0,
                        wx.ALIGN_CENTER_VERTICAL),
                       ((5, 5), 1),
                       (colors[ID_INFO_FORE], 0, wx.EXPAND),
                       ((5, 5), 1),
                       (colors[ID_INFO_BACK], 0, wx.EXPAND),
                       # Fifth Row
                       (wx.StaticText(self, label=_("Warning Text") + u":"), 0,
                        wx.ALIGN_CENTER_VERTICAL),
                       ((5, 5), 1),
                       (colors[ID_WARN_FORE], 0, wx.EXPAND),
                       ((5, 5), 1),
                       (colors[ID_WARN_BACK], 0, wx.EXPAND)])
        boxsz.Add(flexg, 0, wx.EXPAND)

        # Layout
        msizer.AddMany([((5, 5), 0),
                        (wx.StaticText(self, label=("Actions") + u":"), 0),
                        ((5, 5), 0), (clear_cb, 0),
                        ((10, 10), 0), (wx.StaticLine(self), 0, wx.EXPAND),
                        ((10, 10), 0),
                        (boxsz, 1, wx.EXPAND)])
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddMany([((5, 5), 0), (msizer, 1, wx.EXPAND), ((5, 5), 0)])
        self.SetSizer(hsizer)

    def OnCheck(self, evt):
        """Handle checkbox events"""
        e_id = evt.GetId()
        e_val = evt.GetEventObject().GetValue()
        cfg = Profile_Get(LAUNCH_PREFS, default=dict())
        if e_id == ID_AUTOCLEAR:
            cfg['autoclear'] = e_val
        else:
            evt.Skip()

    def OnColor(self, evt):
        """Handle color change events"""
        e_id = evt.GetId()
        color = COLOR_MAP.get(e_id, None)
        if color is not None:
            Profile_Get(LAUNCH_PREFS)[color] = evt.GetValue().Get()
        else:
            evt.Skip()

#-----------------------------------------------------------------------------#
ID_BROWSE = wx.NewId()

class CommandListCtrl(listmix.ListCtrlAutoWidthMixin,
                      listmix.TextEditMixin,
                      eclib.ListRowHighlighter,
#                      listmix.CheckListCtrlMixin,
                      wx.ListCtrl):
    """Auto-width adjusting list for showing editing the commands"""
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
#        listmix.CheckListCtrlMixin.__init__(self)
        eclib.ListRowHighlighter.__init__(self)

        # Attributes
        self._menu = None
        self._cindex = -1

        # Setup
        self.SetToolTipString(_("Click on an item to edit"))
#        pcol = _("Dir")
#        self.InsertColumn(0, pcol)
        self.InsertColumn(0, _("Alias"))
        self.InsertColumn(1, _("Executable Commands"))
#        self.SetColumnWidth(0, self.GetTextExtent(pcol)[0] + 5)

        listmix.TextEditMixin.__init__(self)

        # Event Handlers
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnContextClick)
        self.Bind(wx.EVT_MENU, self.OnMenu, id=ID_BROWSE)

    def OnContextClick(self, evt):
        """Handle right clicks"""
        if not self.GetSelectedItemCount():
            evt.Skip()
            return

        if self._menu is None:
            # Lazy init of menu
            self._menu = wx.Menu()
            self._menu.Append(ID_BROWSE, _("Browse"))

        self._cindex = evt.GetIndex()
        self.PopupMenu(self._menu)

    def OnMenu(self, evt):
        """Handle Menu events"""
        e_id = evt.GetId()
        if e_id == ID_BROWSE:
            dlg = wx.FileDialog(self, _("Choose and executable"))
            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                if self._cindex >= 0:
                    self.SetStringItem(self._cindex, 1, path)
                    levt = wx.ListEvent(wx.wxEVT_COMMAND_LIST_END_LABEL_EDIT,
                                        self.GetId())
# TODO: ERR ><! there are no setters for index, column, and label...
#                    levt.Index = self._cindex
#                    levt.SetInt(self._cindex)
#                    levt.Column = 1
#                    levt.Label = path
                    # HACK set the member variables directly...
                    levt.m_itemIndex = self._cindex
                    levt.m_col = 1
                    levt.SetString(path)
                    wx.PostEvent(self.GetParent(), levt)
        else:
            evt.Skip()

#    def Append(self, entry):
#        """Append a row to the list. Overrides ListCtrl.Append to allow
#        for setting a bool on the first object to check or uncheck the
#        checkbox on the first column.
#        @param entry: tuple (bool, string, string)

#        """
#        check, alias, cmd = entry
#        wx.ListCtrl.Append(self, ('', alias, cmd))
#        self.CheckItem(self.GetItemCount() - 1, check)

#    def OpenEditor(self, col, row):
#        """Disable the editor for the first column
#        @param col: Column to edit
#        @param row: Row to edit

#        """
#        if col != 0:
#            listmix.TextEditMixin.OpenEditor(self, col, row)
#        else:
#            # Handle the checkbox click
#            self.CheckItem(row, not self.IsChecked(row))

#    def OnCheckItem(self, index, flag):
#        """Override CheckListMixin to update handlers
#        @param index: list index
#        @param flag: check or uncheck

#        """
#        parent = self.GetParent()
#        parent.UpdateCurrentHandler(index)

#-----------------------------------------------------------------------------#

def GetHandlerTypes():
    """Get the language type handlers for each language that
    has a handler defined.
    @return: list of handler names

    """
    keys = handlers.HANDLERS.keys()
    keys.remove(0)
    rlist = list()
    for key in keys:
        handle = handlers.HANDLERS[key]
        rlist.append(handle.GetName().title())
    return sorted(rlist)
