# -*- coding: utf-8 -*-
###############################################################################
# Name: launch.py                                                             #
# Purpose: Launch Ui                                                          #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""Launch User Interface"""
__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: launch.py 59917 2009-03-29 17:51:59Z CJP $"
__revision__ = "$Revision: 59917 $"
__version__ = "0.1"

#-----------------------------------------------------------------------------#
# Imports
import os
import wx
import wx.stc

# Local Imports
import handlers
import cfgdlg

# Editra Libraries
import ed_glob
import util
from profiler import Profile_Get, Profile_Set
import ed_msg
import eclib

#-----------------------------------------------------------------------------#
# Globals
ID_SETTINGS = wx.NewId()
ID_EXECUTABLE = wx.NewId()
ID_ARGS = wx.NewId()
ID_RUN = wx.NewId()

# Profile Settings Key
LAUNCH_KEY = 'Launch.Config'
#LAUNCH_PREFS = 'Launch.Prefs' # defined in cfgdlg

# Custom Messages
MSG_RUN_LAUNCH = ('launch', 'run')
MSG_RUN_LAST = ('launch', 'runlast')

# Value request messages
REQUEST_ACTIVE = 'Launch.IsActive'
REQUEST_RELAUNCH = 'Launch.CanRelaunch'

_ = wx.GetTranslation
#-----------------------------------------------------------------------------#

def OnStoreConfig(msg):
    Profile_Set(LAUNCH_KEY, handlers.GetState())
ed_msg.Subscribe(OnStoreConfig, cfgdlg.EDMSG_LAUNCH_CFG_EXIT)

#-----------------------------------------------------------------------------#

class LaunchWindow(eclib.ControlBox):
    """Control window for showing and running scripts"""
    def __init__(self, parent):
        eclib.ControlBox.__init__(self, parent)

        # Attributes
        self._mw = self.__FindMainWindow()
        self._buffer = OutputDisplay(self)
        self._fnames = list()
        self._chFiles = None # Created in __DoLayout
        self._worker = None
        self._busy = False
        self._isready = False
        self._config = dict(file='', lang=0,
                            cfile='', clang=0,
                            last='', lastlang=0,
                            prelang=0, largs='',
                            lcmd='')
        self._prefs = Profile_Get(cfgdlg.LAUNCH_PREFS, default=None)

        # Setup
        self.__DoLayout()
        hstate = Profile_Get(LAUNCH_KEY)
        if hstate is not None:
            handlers.SetState(hstate)
        if self._prefs is None:
            Profile_Set(cfgdlg.LAUNCH_PREFS,
                        dict(autoclear=False,
                             defaultf=self._buffer.GetDefaultForeground().Get(),
                             defaultb=self._buffer.GetDefaultBackground().Get(),
                             errorf=self._buffer.GetErrorForeground().Get(),
                             errorb=self._buffer.GetErrorBackground().Get(),
                             infof=self._buffer.GetInfoForeground().Get(),
                             infob=self._buffer.GetInfoBackground().Get(),
                             warnf=self._buffer.GetWarningForeground().Get(),
                             warnb=self._buffer.GetWarningBackground().Get()))
            self._prefs = Profile_Get(cfgdlg.LAUNCH_PREFS)

        self.UpdateBufferColors()
        cbuffer = self._mw.GetNotebook().GetCurrentCtrl()
        self.SetupControlBar(cbuffer)
        self._config['lang'] = GetLangIdFromMW(self._mw)
        self.UpdateCurrentFiles(self._config['lang'])
        self.SetFile(GetTextBuffer(self._mw).GetFileName())

        # Setup filetype settings
        self.RefreshControlBar()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)
        self.Bind(wx.EVT_CHOICE, self.OnChoice)
        ed_msg.Subscribe(self.OnPageChanged, ed_msg.EDMSG_UI_NB_CHANGED)
        ed_msg.Subscribe(self.OnFileOpened, ed_msg.EDMSG_FILE_OPENED)
        ed_msg.Subscribe(self.OnThemeChanged, ed_msg.EDMSG_THEME_CHANGED)
        ed_msg.Subscribe(self.OnLexerChange, ed_msg.EDMSG_UI_STC_LEXER)
        ed_msg.Subscribe(self.OnConfigExit, cfgdlg.EDMSG_LAUNCH_CFG_EXIT)
        ed_msg.Subscribe(self.OnRunMsg, MSG_RUN_LAUNCH)
        ed_msg.Subscribe(self.OnRunLastMsg, MSG_RUN_LAST)
        ed_msg.RegisterCallback(self._CanLaunch, REQUEST_ACTIVE)
        ed_msg.RegisterCallback(self._CanReLaunch, REQUEST_RELAUNCH)

    def __del__(self):
        ed_msg.Unsubscribe(self.OnPageChanged)
        ed_msg.Unsubscribe(self.OnFileOpened)
        ed_msg.Unsubscribe(self.OnThemeChanged)
        ed_msg.Unsubscribe(self.OnLexerChange)
        ed_msg.Unsubscribe(self.OnConfigExit)
        ed_msg.Unsubscribe(self.OnRunMsg)
        ed_msg.Unsubscribe(self.OnRunLastMsg)
        ed_msg.UnRegisterCallback(self._CanLaunch)
        ed_msg.UnRegisterCallback(self._CanReLaunch)
        super(LaunchWindow, self).__del__()

    def __DoLayout(self):
        """Layout the window"""
        #-- Setup ControlBar --#
        ctrlbar = eclib.ControlBar(self, style=eclib.CTRLBAR_STYLE_GRADIENT)
        if wx.Platform == '__WXGTK__':
            ctrlbar.SetWindowStyle(eclib.CTRLBAR_STYLE_DEFAULT)

        # Preferences
        prefbmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_PREF), wx.ART_MENU)
        pref = eclib.PlateButton(ctrlbar, ID_SETTINGS, '', prefbmp,
                                 style=eclib.PB_STYLE_NOBG)
        pref.SetToolTipString(_("Settings"))
        ctrlbar.AddControl(pref, wx.ALIGN_LEFT)

        # Exe
        ctrlbar.AddControl(wx.StaticText(ctrlbar, label=_("exec") + ":"),
                           wx.ALIGN_LEFT)
        exe = wx.Choice(ctrlbar, ID_EXECUTABLE)
        exe.SetToolTipString(_("Program Executable Command"))
        ctrlbar.AddControl(exe, wx.ALIGN_LEFT)

        # Script Label
        ctrlbar.AddControl((5, 5), wx.ALIGN_LEFT)
        self._chFiles = wx.Choice(ctrlbar, choices=[''])
        ctrlbar.AddControl(self._chFiles, wx.ALIGN_LEFT)

        # Args
        ctrlbar.AddControl((5, 5), wx.ALIGN_LEFT)
        ctrlbar.AddControl(wx.StaticText(ctrlbar, label=_("args") + ":"),
                           wx.ALIGN_LEFT)
        args = wx.TextCtrl(ctrlbar, ID_ARGS)
        args.SetToolTipString(_("Script Arguments"))
        ctrlbar.AddControl(args, wx.ALIGN_LEFT)

        # Spacer
        ctrlbar.AddStretchSpacer()
        
        # Run Button
        rbmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_BIN_FILE), wx.ART_MENU)
        if rbmp.IsNull() or not rbmp.IsOk():
            rbmp = None
        run = eclib.PlateButton(ctrlbar, ID_RUN, _("Run"), rbmp,
                                style=eclib.PB_STYLE_NOBG)
        ctrlbar.AddControl(run, wx.ALIGN_RIGHT)

        # Clear Button
        cbmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_DELETE), wx.ART_MENU)
        if cbmp.IsNull() or not cbmp.IsOk():
            cbmp = None
        clear = eclib.PlateButton(ctrlbar, wx.ID_CLEAR, _("Clear"),
                                  cbmp, style=eclib.PB_STYLE_NOBG)
        ctrlbar.AddControl(clear, wx.ALIGN_RIGHT)
        ctrlbar.SetVMargin(1, 1)
        self.SetControlBar(ctrlbar)

        self.SetWindow(self._buffer)

    def __FindMainWindow(self):
        """Find the mainwindow of this control
        @return: MainWindow or None

        """
        def IsMainWin(win):
            """Check if the given window is a main window"""
            return getattr(tlw, '__name__', '') == 'MainWindow'

        tlw = self.GetTopLevelParent()
        if IsMainWin(tlw):
            return tlw
        elif hasattr(tlw, 'GetParent'):
            tlw = tlw.GetParent()
            if IsMainWin(tlw):
                return tlw

        return None

    def _CanLaunch(self):
        """Method to use with RegisterCallback for getting status"""
        val = self.CanLaunch()
        if not val:
            val = ed_msg.NullValue()
        return val

    def _CanReLaunch(self):
        """Method to use with RegisterCallback for getting status"""
        val = self.CanLaunch()
        if not val or not len(self._config['last']):
            val = ed_msg.NullValue()
        return val

    def CanLaunch(self):
        """Can the launch window run or not
        @return: bool

        """
        parent = self.GetParent()
        return parent.GetParent().IsActive() and self._isready

    def GetFile(self):
        """Get the file that is currently set to be run
        @return: file path

        """
        return self._config['file']

    def GetLastRun(self):
        """Get the last file that was run
        @return: (fname, lang_id)

        """
        return (self._config['last'], self._config['lastlang'])

    def GetMainWindow(self):
        """Get the mainwindow that created this instance
        @return: reference to MainWindow

        """
        return self._mw

    def OnButton(self, evt):
        """Handle events from the buttons on the control bar"""
        e_id = evt.GetId()
        if e_id == ID_SETTINGS:
            app = wx.GetApp()
            win = app.GetWindowInstance(cfgdlg.ConfigDialog)
            if win is None:
                config = cfgdlg.ConfigDialog(self._mw)
                config.CentreOnParent()
                config.Show()
            else:
                win.Raise()
        elif e_id == ID_RUN:
            # May be run or abort depending on current state
            self.StartStopProcess()
        elif e_id == wx.ID_CLEAR:
            self._buffer.Clear()
        else:
            evt.Skip()

    def OnChoice(self, evt):
        """Handle events from the Choice controls
        @param evt: wx.CommandEvent

        """
        e_id = evt.GetId()
        e_sel = evt.GetSelection()
        if e_id == self._chFiles.GetId():
            fname = self._fnames[e_sel]
            self.SetFile(fname)
            self._chFiles.SetToolTipString(fname)
        elif e_id == ID_EXECUTABLE:
            e_obj = evt.GetEventObject()
            handler = handlers.GetHandlerById(self._config['lang'])
            cmd = e_obj.GetStringSelection()
            e_obj.SetToolTipString(handler.GetCommand(cmd))
        else:
            evt.Skip()

    def OnConfigExit(self, msg):
        """Update current state when the config dialog has been closed
        @param msg: Message Object

        """
        util.Log("[Launch][info] Saving config to profile")
        self.RefreshControlBar()
        Profile_Set(LAUNCH_KEY, handlers.GetState())
        self.UpdateBufferColors()

    def OnFileOpened(self, msg):
        """Reset state when a file open message is recieved
        @param msg: Message Object

        """
        # Only update when in the active window
        if not self._mw.IsActive():
            return

        # Update the file choice control
        self._config['lang'] = GetLangIdFromMW(self._mw)
        self.UpdateCurrentFiles(self._config['lang'])

        fname = msg.GetData()
        self.SetFile(fname)

        # Setup filetype settings
        self.RefreshControlBar()

    def OnLexerChange(self, msg):
        """Update the status of the currently associated file
        when a file is saved. Used for updating after a file type has
        changed due to a save action.
        @param msg: Message object

        """
        if not self._mw.IsActive():
            return

        mdata = msg.GetData()
        # For backwards compatibility with older message format
        if mdata is None:
            return

        fname, ftype = msg.GetData()
        if ftype != self._config['lang']:
            self.UpdateCurrentFiles(ftype)
            self.SetControlBarState(fname, ftype)

    def OnPageChanged(self, msg):
        """Update the status of the currently associated file
        when the page changes in the main notebook.
        @param msg: Message object

        """
        # Only update when in the active window
        if not self._mw.IsActive():
            return

        mval = msg.GetData()
        ctrl = mval[0].GetCurrentCtrl()
        self.UpdateCurrentFiles(ctrl.GetLangId())
        if hasattr(ctrl, 'GetFileName'):
            self.SetupControlBar(ctrl)

    def OnRunMsg(self, msg):
        """Run or abort a launch process if this is the current 
        launch window.
        @param msg: MSG_RUN_LAUNCH

        """
        if self.CanLaunch():
            shelf = self._mw.GetShelf()
            shelf.RaiseWindow(self)
            self.StartStopProcess()

    def OnRunLastMsg(self, msg):
        """Re-run the last run program.
        @param msg: MSG_RUN_LAST

        """
        if self.CanLaunch():
            fname, ftype = self.GetLastRun()
            # If there is no last run file return
            if not len(fname):
                return

            shelf = self._mw.GetShelf()
            self.UpdateCurrentFiles(ftype)
            self.SetFile(fname)
            self.RefreshControlBar()
            shelf.RaiseWindow(self)

            if self._prefs.get('autoclear'):
                self._buffer.Clear()

            self.SetProcessRunning(True)

            self.Run(fname, self._config['lcmd'], self._config['largs'], ftype)

    def OnThemeChanged(self, msg):
        """Update icons when the theme has been changed
        @param msg: Message Object

        """
        ctrls = ((ID_SETTINGS, ed_glob.ID_PREF),
                 (wx.ID_CLEAR, ed_glob.ID_DELETE))
        if self._busy:
            ctrls += ((ID_RUN, ed_glob.ID_STOP),)
        else:
            ctrls += ((ID_RUN, ed_glob.ID_BIN_FILE),)

        for ctrl, art in ctrls:
            btn = self.FindWindowById(ctrl)
            bmp = wx.ArtProvider.GetBitmap(str(art), wx.ART_MENU)
            btn.SetBitmap(bmp)
            btn.Refresh()

    def RefreshControlBar(self):
        """Refresh the state of the control bar based on the current config"""
        handler = handlers.GetHandlerById(self._config['lang'])
        cmds = handler.GetAliases()

        # Get the controls
        exe_ch = self.FindWindowById(ID_EXECUTABLE)
        args_txt = self.FindWindowById(ID_ARGS)
        run_btn = self.FindWindowById(ID_RUN)

        # Set control states
        csel = exe_ch.GetStringSelection()
        exe_ch.SetItems(cmds)
        if len(cmds):
            exe_ch.SetToolTipString(handler.GetCommand(cmds[0]))

        util.Log("[Launch][info] Found commands %s" % str(cmds))
        if handler.GetName() != handlers.DEFAULT_HANDLER and len(self.GetFile()):
            for ctrl in (exe_ch, args_txt, run_btn, self._chFiles):
                ctrl.Enable()
            self._isready = True

            if self._config['lang'] == self._config['prelang'] and len(csel):
                exe_ch.SetStringSelection(csel)
            else:
                csel = handler.GetDefault()
                exe_ch.SetStringSelection(csel)

            exe_ch.SetToolTipString(handler.GetCommand(csel))
            self.GetControlBar().Layout()
        else:
            self._isready = False
            for ctrl in (exe_ch, args_txt, run_btn, self._chFiles):
                ctrl.Disable()

    def Run(self, fname, cmd, args, ftype):
        """Run the given file
        @param fname: File path
        @param cmd: Command to run on file
        @param args: Executable arguments
        @param ftype: File type id

        """
        # Find and save the file if it is modified
        nb = self._mw.GetNotebook()
        for ctrl in nb.GetTextControls():
            tname = ctrl.GetFileName()
            if fname == tname:
                if ctrl.GetModify():
                    ctrl.SaveFile(tname)
                    break

        handler = handlers.GetHandlerById(ftype)
        path, fname = os.path.split(fname)
        self._worker = eclib.ProcessThread(self._buffer,
                                           cmd, fname,
                                           args, path,
                                           handler.GetEnvironment())
        self._worker.start()

    def StartStopProcess(self):
        """Run or abort the context of the current process if possible"""
        if self._prefs.get('autoclear'):
            self._buffer.Clear()

        self.SetProcessRunning(not self._busy)
        if self._busy:
            util.Log("[Launch][info] Starting process")
            handler = handlers.GetHandlerById(self._config['lang'])
            cmd = self.FindWindowById(ID_EXECUTABLE).GetStringSelection()
            self._config['lcmd'] = cmd
            cmd = handler.GetCommand(cmd)
            args = self.FindWindowById(ID_ARGS).GetValue().split()
            self._config['largs'] = args
            self.Run(self._config['file'], cmd, args, self._config['lang'])
        else:
            util.Log("[Launch][info] Aborting process")
            self._worker.Abort()
            self._worker = None

    def SetFile(self, fname):
        """Set the script file that will be run
        @param fname: file path

        """
        # Set currently selected file
        self._config['file'] = fname
        self._chFiles.SetStringSelection(os.path.split(fname)[1])
        self.GetControlBar().Layout()

    def SetLangId(self, langid):
        """Set the language id value(s)
        @param langid: syntax.synglob lang id

        """
        self._config['prelang'] = self._config['lang']
        self._config['lang'] = langid

    def SetProcessRunning(self, running=True):
        """Set the state of the window into either process running mode
        or process not running mode.
        @keyword running: Is a process running or not

        """
        rbtn = self.FindWindowById(ID_RUN)
        self._busy = running
        if running:
            self._config['last'] = self._config['file']
            self._config['lastlang'] = self._config['lang']
            self._config['cfile'] = self._config['file']
            self._config['clang'] = self._config['lang']
            abort = wx.ArtProvider.GetBitmap(str(ed_glob.ID_STOP), wx.ART_MENU)
            if abort.IsNull() or not abort.IsOk():
                abort = wx.ArtProvider.GetBitmap(wx.ART_ERROR,
                                                 wx.ART_MENU, (16, 16))
            rbtn.SetBitmap(abort)
            rbtn.SetLabel(_("Abort"))
        else:
            rbmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_BIN_FILE), wx.ART_MENU)
            if rbmp.IsNull() or not rbmp.IsOk():
                rbmp = None
            rbtn.SetBitmap(rbmp)
            rbtn.SetLabel(_("Run"))
            # If the buffer was changed while this was running we should
            # update to the new buffer now that it has stopped.
            self.SetFile(self._config['cfile'])
            self.SetLangId(self._config['clang'])
            self.RefreshControlBar()

        self.GetControlBar().Layout()
        rbtn.Refresh()

    def SetupControlBar(self, ctrl):
        """Set the state of the controlbar based data found in the buffer
        passed in.
        @param ctrl: EdStc

        """
        fname = ctrl.GetFileName()
        lang_id = ctrl.GetLangId()
        self.SetControlBarState(fname, lang_id)

    def SetControlBarState(self, fname, lang_id):
        # Don't update the bars status if the buffer is busy
        if self._buffer.IsRunning():
            self._config['cfile'] = fname
            self._config['clang'] = lang_id
        else:
            self.SetFile(fname)
            self.SetLangId(lang_id)

            # Refresh the control bars view
            self.RefreshControlBar()

    def UpdateBufferColors(self):
        """Update the buffers colors"""
        colors = dict()
        for color in ('defaultf', 'defaultb', 'errorf', 'errorb',
                      'infof', 'infob', 'warnf', 'warnb'):
            val = self._prefs.get(color, None)
            if val is not None:
                colors[color] = wx.Colour(*val)
            else:
                colors[color] = val

        self._buffer.SetDefaultColor(colors['defaultf'], colors['defaultb'])
        self._buffer.SetErrorColor(colors['errorf'], colors['errorb'])
        self._buffer.SetInfoColor(colors['infof'], colors['infob'])
        self._buffer.SetWarningColor(colors['warnf'], colors['warnb'])

    def UpdateCurrentFiles(self, lang_id):
        """Update the current set of open files that are of the same
        type.
        @param lang_id: Editra filetype id
        @postcondition: all open files that are of the same type are set
                        and stored in the file choice control.

        """
        self._fnames = list()
        for txt_ctrl in self._mw.GetNotebook().GetTextControls():
            if lang_id == txt_ctrl.GetLangId():
                self._fnames.append(txt_ctrl.GetFileName())

        items = [ os.path.basename(fname) for fname in self._fnames ]
        try:
            self._chFiles.SetItems(items)
            if len(self._fnames):
                self._chFiles.SetToolTipString(self._fnames[0])
        except TypeError:
            util.Log("[Launch][err] UpdateCurrent Files: " + str(items))
            self._chFiles.SetItems([''])

#-----------------------------------------------------------------------------#

class OutputDisplay(eclib.OutputBuffer, eclib.ProcessBufferMixin):
    """Main output buffer display"""
    def __init__(self, parent):
        eclib.OutputBuffer.__init__(self, parent)
        eclib.ProcessBufferMixin.__init__(self)

        # Attributes
        self._mw = parent.GetMainWindow()
        self._cfile = ''

        # Setup
        font = Profile_Get('FONT1', 'font', wx.Font(11, wx.FONTFAMILY_MODERN,
                                                    wx.FONTSTYLE_NORMAL,
                                                    wx.FONTWEIGHT_NORMAL))
        self.SetFont(font)

    def ApplyStyles(self, start, txt):
        """Apply any desired output formatting to the text in
        the buffer.
        @param start: Start position of new text
        @param txt: the new text that was added to the buffer

        """
        handler = self.GetCurrentHandler()
        handler.StyleText(self, start, txt)

    def DoFilterInput(self, txt):
        """Filter the incoming input
        @param txt: incoming text to filter

        """
        handler = self.GetCurrentHandler()
        return handler.FilterInput(txt)

    def DoHotSpotClicked(self, pos, line):
        """Pass hotspot click to the filetype handler for processing
        @param pos: click position
        @param line: line the click happened on
        @note: overridden from L{eclib.OutputBuffer}

        """
        fname, lang_id = self.GetParent().GetLastRun()
        handler = handlers.GetHandlerById(lang_id)
        handler.HandleHotSpot(self._mw, self, line, fname)
        self.GetParent().SetupControlBar(GetTextBuffer(self._mw))

    def DoProcessExit(self, code=0):
        """Do all that is needed to be done after a process has exited"""
        self.AppendUpdate(">>> %s: %d%s" % (_("Exit Code"), code, os.linesep))
        self.Stop()
        self.GetParent().SetProcessRunning(False)

    def DoProcessStart(self, cmd=''):
        """Do any necessary preprocessing before a process is started"""
        self.GetParent().SetProcessRunning(True)
        self.AppendUpdate(">>> %s%s" % (cmd, os.linesep))

    def GetCurrentHandler(self):
        """Get the current filetype handler
        @return: L{handlers.FileTypeHandler} instance

        """
        lang_id = self.GetParent().GetLastRun()[1]
        handler = handlers.GetHandlerById(lang_id)
        return handler

#-----------------------------------------------------------------------------#
def GetLangIdFromMW(mainw):
    """Get the language id of the file in the current buffer
    in Editra's MainWindow.
    @param mainw: mainwindow instance

    """
    ctrl = GetTextBuffer(mainw)
    if hasattr(ctrl, 'GetLangId'):
        return ctrl.GetLangId()

def GetTextBuffer(mainw):
    """Get the current text buffer of the current window"""
    nb = mainw.GetNotebook()
    return nb.GetCurrentCtrl()
