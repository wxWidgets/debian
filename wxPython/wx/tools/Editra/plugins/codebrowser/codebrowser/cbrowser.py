###############################################################################
# Name: cbrowser.py                                                           #
# Purpose: CodeBrowser UI                                                     #
# Author: Cody Precord <cprecord@editra.org>                                  #
# Copyright: (c) 2008 Cody Precord <staff@editra.org>                         #
# License: wxWindows License                                                  #
###############################################################################

"""
FILE: cbrowser.py
AUTHOR: Cody Precord
LANGUAGE: Python
SUMMARY:
    CodeBrowser UI, displays the DocStruct object returned by the L{gentag} lib
as a tree. Clicking on the elements in the tree will navigate to where the
element is defined in the file.

"""

__author__ = "Cody Precord <cprecord@editra.org>"
__svnid__ = "$Id: cbrowser.py 60379 2009-04-26 05:24:41Z CJP $"
__revision__ = "$Revision: 60379 $"

#--------------------------------------------------------------------------#
# Imports
import StringIO
import threading
import wx

# Editra Libraries
import ed_glob
from profiler import Profile_Get, Profile_Set
import ed_msg

# Local Imports
import gentag.taglib as taglib
from tagload import TagLoader
import IconFile

#--------------------------------------------------------------------------#
# Globals
ID_CODEBROWSER = wx.NewId()
ID_BROWSER = wx.NewId()
ID_GOTO_ELEMENT = wx.NewId()
PANE_NAME = u"CodeBrowser"
_ = wx.GetTranslation

# HACK for i18n scripts to pick up translation strings
STRINGS = ( _("Class Definitions"), _("Defines"), _("Function Definitions"),
            _("Global Variables"), _("Identities"), _("Labels"), _("Macros"),
            _("Macro Definitions"), _("Namespaces"), _("Packages"),
            _("Procedure Definitions"), _("Programs"), _("Protocols"),
            _("Sections"), _("Style Tags"), _("Subroutines"),
            _("Subroutine Declarations"), _("Task Definitions"), 
            _("Modules"), _("Functions"), _("Public Functions"),
            _("Public Subroutines") )
del STRINGS

#--------------------------------------------------------------------------#

class CodeBrowserTree(wx.TreeCtrl):
    def __init__(self, parent, id=ID_BROWSER,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT):
        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)

        # Attributes
        self._mw = parent
        self._menu = None
        self._selected = None
        self._cjob = 0
        self._lastjob = u'' # Name of file in last sent out job
        self._cdoc = None   # Current DocStruct
        self.icons = dict()
        self.il = None

        self._timer = wx.Timer(self)
        self._cpage = None
        self._force = False

        # Setup
        self._SetupImageList()
        viewm = self._mw.GetMenuBar().GetMenuByName("view")
        self._mi = viewm.InsertAlpha(ID_CODEBROWSER, _("Code Browser"), 
                                     _("Open Code Browser Sidepanel"),
                                     wx.ITEM_CHECK,
                                     after=ed_glob.ID_PRE_MARK)

        self.root = self.AddRoot('CodeBrowser')
        self.SetPyData(self.root, None)
        self.SetItemImage(self.root, self.icons['class'])
        self.nodes = dict(globals=None, classes=None, funct=None)

        # Event Handlers
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivated)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnContext)
        self.Bind(wx.EVT_MENU, self.OnMenu)
        self.Bind(wx.EVT_TIMER, self.OnStartJob)
        self.Bind(EVT_JOB_FINISHED, self.OnTagsReady)
        ed_msg.Subscribe(self.OnThemeChange, ed_msg.EDMSG_THEME_CHANGED)
        ed_msg.Subscribe(self.OnUpdateTree, ed_msg.EDMSG_UI_NB_CHANGED)
        ed_msg.Subscribe(self.OnUpdateTree, ed_msg.EDMSG_FILE_OPENED)
        ed_msg.Subscribe(self.OnUpdateTree, ed_msg.EDMSG_FILE_SAVED)

        # Backwards compatibility
        if hasattr(ed_msg, 'EDMSG_UI_STC_LEXER') and \
           hasattr(ed_msg, 'EDMSG_DSP_FONT'):
            ed_msg.Subscribe(self.OnUpdateFont, ed_msg.EDMSG_DSP_FONT)
            ed_msg.Subscribe(self.OnUpdateTree, ed_msg.EDMSG_UI_STC_LEXER)

    def __del__(self):
        """Unsubscribe from messages on del"""
        ed_msg.Unsubscribe(self.OnUpdateTree)
        ed_msg.Unsubscribe(self.OnThemeChange)
        ed_msg.Unsubscribe(self.OnUpdateFont)

    def _GetCurrentCtrl(self):
        """Get the current buffer"""
        return self._mw.GetNotebook().GetCurrentCtrl()

    def _SetupImageList(self):
        """Setup the image list for the tree"""
        imglst = wx.ImageList(16, 16)

        globe = wx.ArtProvider.GetBitmap(str(ed_glob.ID_WEB), wx.ART_MENU)
        self.icons['globals'] = imglst.Add(globe)

        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_CLASS_TYPE), wx.ART_MENU)
        self.icons['class'] = imglst.Add(bmp)
        self.icons['section'] = imglst.Add(IconFile.Brick_Add.GetBitmap())
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_FUNCT_TYPE), wx.ART_MENU)
        self.icons['function'] = imglst.Add(bmp)
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_METHOD_TYPE), wx.ART_MENU)
        self.icons['method'] = imglst.Add(bmp)
        self.icons['subroutine'] = self.icons['function']
        self.icons['procedure'] = self.icons['function']
        self.icons['task'] = imglst.Add(bmp)
        self.icons['function2'] = self.icons['task']
        bmp = wx.ArtProvider.GetBitmap(str(ed_glob.ID_VARIABLE_TYPE), wx.ART_MENU)
        self.icons['variable'] = imglst.Add(bmp)
        self.icons['namespace'] = imglst.Add(IconFile.Brick_Bricks.GetBitmap())
        self.icons['tag_red'] = imglst.Add(IconFile.Tag_Red.GetBitmap())
        self.icons['tag_blue'] = imglst.Add(IconFile.Tag_Blue.GetBitmap())
        self.icons['tag_green'] = imglst.Add(IconFile.Tag_Green.GetBitmap())
        self.SetImageList(imglst)
        # NOTE: Must save reference to the image list or tree will crash!!!
        self.il = imglst

    def _GetIconIndex(self, cobj):
        """Get the index of an appropriate icon for the given code object
        @param cobj: L{taglib.Code} object
        @return: int

        """
        img = self.icons.get(cobj.type, None)
        if img is None:
            if isinstance(cobj, taglib.Function):
                img = self.icons['function']
            elif isinstance(cobj, taglib.Scope):
                img = self.icons['section']
            else:
                img = self.icons['variable']
        return img

    def _ShouldUpdate(self):
        """Check whether the tree should do an update or not
        @return: bool

        """
        pane = self._mw.GetFrameManager().GetPane(PANE_NAME)
        if self._mw.IsExiting() or not pane.IsShown():
            return False
        else:
            return True

    def AppendClass(self, cobj):
        """Append a class node to the tree
        @param cobj: Class item object

        """
        if self.nodes.get('classes', None) is None:
            croot = self.AppendItem(self.GetRootItem(), _("Class Definitions"))
            self.SetItemHasChildren(croot)
            self.SetPyData(croot, None)
            self.SetItemImage(croot, self.icons['class'])
            self.nodes['classes'] = croot

        croot = self.AppendCodeObj(self.nodes['classes'], cobj, self.icons['class'])

    def AppendCodeObj(self, node, cobj, img):
        """Append a code object to the given node and set its data
        @param node: node to attach object to
        @param cobj: code object
        @return: tree item id

        """
        item_id = self.AppendItem(node, u"%s [%d]" % (cobj.GetName(), 1 + cobj.GetLine()), img)
        self.SetPyData(item_id, cobj.GetLine())
        # If the item is a scope it may have sub items
        if isinstance(cobj, taglib.Scope):
            elements = cobj.GetElements()
            if len(elements):
                self.SetItemHasChildren(item_id)
                for elem in elements: # Ordered list of dict objects
                    for otype in elem[elem.keys()[0]]:
                        img = self._GetIconIndex(otype)
                        # Make recursive call as Scope's may contain other
                        # Scopes.
                        self.AppendCodeObj(item_id, otype, img)
        return item_id

    def AppendGlobal(self, gobj):
        """Append a global variable/object to the Globals node
        @param gobj: Object derived from Scope

        """
        if self.nodes.get('globals', None) is None:
            desc = self._cdoc.GetElementDescription('variable')
            if desc == 'variable':
                desc = "Global Variables"
            self.nodes['globals']  = self.AppendItem(self.GetRootItem(), _(desc))
            self.SetItemHasChildren(self.nodes['globals'])
            self.SetPyData(self.nodes['globals'], None)
            self.SetItemImage(self.nodes['globals'], self.icons['globals'])

        self.AppendCodeObj(self.nodes['globals'], gobj, self.icons['variable'])

    def AppendElement(self, obj):
        """Append a general code object to the document
        @param obj: Code object

        """
        # Check if there is a node for this Code object
        if self.nodes.get(obj.type, None) is None:
            # Look for a description to use as catagory title
            if self._cdoc is not None:
                desc = self._cdoc.GetElementDescription(obj.type).title()
            else:
                desc = obj.type.title()

            self.nodes[obj.type] = self.AppendItem(self.GetRootItem(), _(desc),
                                                   self._GetIconIndex(obj))
            self.SetItemHasChildren(self.nodes[obj.type])
            self.SetPyData(self.nodes[obj.type], None)

        self.AppendCodeObj(self.nodes[obj.type], obj, self._GetIconIndex(obj))

    def DeleteChildren(self, item):
        """Delete the children of a given node"""
        wx.TreeCtrl.DeleteChildren(self, item)
        for key in self.nodes.keys():
            self.nodes[key] = None

    def GotoElement(self, tree_id):
        """Navigate the cursor to the element identified in the
        code browser tree.
        @param tree_id: Tree Id

        """
        line = self.GetPyData(tree_id)
        if line is not None:
            ctrl = self._mw.GetNotebook().GetCurrentCtrl()
            ctrl.GotoLine(line)
            ctrl.SetFocus()

    def OnActivated(self, evt):
        """Handle when an item is clicked on
        @param evt: wx.TreeEvent

        """
        tree_id = evt.GetItem()
        if tree_id is not None:
            self.GotoElement(tree_id)

    def OnContext(self, evt):
        """Show the context menu when an item is clicked on"""
        if self._menu is not None:
            self._menu.Destroy()
            self._menu = None

        tree_id = evt.GetItem()
        data = self.GetPyData(tree_id)
        if data is not None:
            self._selected = tree_id # Store the selected
            self._menu = wx.Menu()
            txt = self.GetItemText(self._selected).split('[')[0].strip()
            self._menu.Append(ID_GOTO_ELEMENT, _("Goto \"%s\"") % txt)
            self.PopupMenu(self._menu)

    def OnCompareItems(self, item1, item2):
        """Compare two tree items for sorting.
        @param item1: wx.TreeItem
        @param item2: wx.TreeItem
        @return: -1, 0, 1

        """
        txt1 = self.GetItemText(item1).lower()
        txt2 = self.GetItemText(item2).lower()
#        txt1 = self.GetPyData(item1)
#        txt2 = self.GetPyData(item2)
        if txt1 < txt2:
            return -1
        elif txt1 == txt2:
            return 0
        else:
            return 1

    def OnMenu(self, evt):
        """Handle the context menu events"""
        if evt.GetId() == ID_GOTO_ELEMENT:
            if self._selected is not None:
                self.GotoElement(self._selected)
        else:
            evt.Skip()

    def OnThemeChange(self, msg):
        """Update the images when Editra's theme changes
        @param msg: Message Object

        """
        self._SetupImageList()
        self.Refresh()

    def OnTagsReady(self, evt):
        """Processing of tag generation has completed, check results
        and update view.
        @param evt: EVT_JOB_FINISHED

        """
        # Make sure that the values that are being returned are the ones for
        # the currently active buffer.
        if evt.GetId() == self._cjob:
            self._lastjob = u''
            self.Freeze()
            self.UpdateAll(evt.GetValue())
            self.Thaw()
            # Stop busy indicator
            ed_msg.PostMessage(ed_msg.EDMSG_PROGRESS_STATE,
                               (self._mw.GetId(), 0, 0))

            if not self._timer.IsRunning():
                self._cpage = None

    def OnUpdateFont(self, msg):
        """Update the ui font when a message comes saying to do so."""
        font = msg.GetData()
        if isinstance(font, wx.Font) and not font.IsNull():
            self.SetFont(font)

    def OnUpdateMenu(self, evt):
        """UpdateUI handler for the panels menu item, to update the check
        mark.
        @param evt: wx.UpdateUIEvent

        """
        pane = self._mw.GetFrameManager().GetPane(PANE_NAME)
        evt.Check(pane.IsShown())

    def OnStartJob(self, evt):
        """Start the tree update job
        @param evt: wxTimerEvent

        """
        if self._cpage is None or not isinstance(self._cpage, wx.Window):
            self._cpage = None
            return
        else:
            # Check if its still the current page
            parent = self._cpage.GetParent()
            if self._cpage != parent.GetCurrentPage():
                return

        # Get the generator method
        genfun = TagLoader.GetGenerator(self._cpage.GetLangId())
        self._cjob += 1 # increment job Id

        # Check if we need to do updates
        if genfun is not None and (self._force or self._ShouldUpdate()):
            self._force = False

            # Start progress indicator in pulse mode
            ed_msg.PostMessage(ed_msg.EDMSG_PROGRESS_SHOW,
                               (self._mw.GetId(), True))
            ed_msg.PostMessage(ed_msg.EDMSG_PROGRESS_STATE,
                               (self._mw.GetId(), -1, -1))

            # Create and start the worker thread
            thread = TagGenThread(self, self._cjob, genfun,
                                  StringIO.StringIO(self._cpage.GetText()))
            wx.CallLater(75, thread.start)
        else:
            self._cdoc = None
            self.DeleteChildren(self.root)
            ed_msg.PostMessage(ed_msg.EDMSG_PROGRESS_SHOW,
                               (self._mw.GetId(), False))
            return

    def OnUpdateTree(self, msg=None, force=False):
        """Update the tree when an action message is sent
        @keyword msg: Message Object
        @keyword force: Force update

        """
        # Don't update when this window is not Active
        istop = wx.GetApp().GetTopWindow() == self._mw
        if not force and not self._mw.IsActive() and not istop:
            return

        page = self._GetCurrentCtrl()
        cfname = page.GetFileName()

        # If its a blank document just clear out
        if not len(cfname):
            self._cdoc = None
            self.DeleteChildren(self.root)
            return

        # If document job is same as current don't start a new one
        if force or self._lastjob != cfname:
            self._lastjob = cfname
            if self._timer.IsRunning():
                self._timer.Stop()

            # Cache the current job information
            self._cpage = page
            self._force = force

            # Start the oneshot timer for beginning the tag generator job
            self._timer.Start(300, True)

    def OnShowBrowser(self, evt):
        """Show the browser pane
        @param evt: wx.MenuEvent

        """
        if evt.GetId() == ID_CODEBROWSER:
            mgr = self._mw.GetFrameManager()
            pane = mgr.GetPane(PANE_NAME)
            pane.Show(not pane.IsShown())
            mgr.Update()
            self.OnUpdateTree(force=True)
        else:
            evt.Skip()

    def UpdateAll(self, tags):
        """Update the entire tree
        @param tags: DocStruct object

        """
        self._cdoc = tags
        self.DeleteChildren(self.root)
        # Check and add any common types in the document first

        # Global Variables
        for var in tags.GetVariables():
            self.AppendGlobal(var)

        # Class Definitions
        for cls in tags.GetClasses():
            self.AppendClass(cls)

        # Check for any remaining custom types of code objects to add
        for element in tags.GetElements():
            for elem in element.values():
                if element.keys()[0] not in ['class', 'variable']:
                    for item in elem:
                        self.AppendElement(item)

        # Expand all main nodes except the one for global variables
        for node in [ node for node in self.nodes.values()
                      if node is not None and node != self.nodes['globals']]:
            self.Expand(node)

#--------------------------------------------------------------------------#
# Tag Generator Thread
class TagGenThread(threading.Thread):
    """Thread for running tag parser on and returning the results for
    display in the tree.

    """
    def __init__(self, reciever, job_id, genfun, buff):
        """Create the thread object
        @param reciever: Window to recieve result
        @param job_id: id of this job
        @param genfun: tag generator function
        @param buff: string buffer to pass to genfun

        """
        threading.Thread.__init__(self)

        # Attributes
        self.reciever = reciever
        self.job = job_id
        self.buff = buff
        self.task = genfun

    def run(self):
        """Run the generator function and return the docstruct to
        the main thread.

        """
        tags = self.task(self.buff)
        evt = TagGenEvent(edEVT_JOB_FINISHED, self.job, tags)
        wx.CallAfter(wx.PostEvent, self.reciever, evt)
        
#--------------------------------------------------------------------------#
# Tag Generator Thread Event(s)

edEVT_JOB_FINISHED = wx.NewEventType()
EVT_JOB_FINISHED = wx.PyEventBinder(edEVT_JOB_FINISHED, 1)

class TagGenEvent(wx.PyCommandEvent):
    """Event to signal when a tag generation job is complete.
    The event id is the job number and the value is the DocStruct
    created by the tag generator

    """
    def __init__(self, etype, eid, value=taglib.DocStruct()):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value
