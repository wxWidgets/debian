/////////////////////////////////////////////////////////////////////////////
// Name:        _taskbar.i
// Purpose:     SWIG interface defs for wxTaskBarIcon
//
// Author:      Robin Dunn
//
// Created:     2-June-1998
// RCS-ID:      $Id: _taskbar.i 67953 2011-06-16 01:25:15Z RD $
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


//---------------------------------------------------------------------------

%{
%}

//---------------------------------------------------------------------------
%newgroup;


%{
enum wxPyTaskBarIconType
{
    wxTBI_DOCK,
    wxTBI_CUSTOM_STATUS_ITEM,
    wxTBI_DEFAULT = wxTBI_CUSTOM_STATUS_ITEM
};

    
#ifndef wxHAS_TASK_BAR_ICON
// implement dummy classes for platforms that don't have it

class wxTaskBarIcon : public wxEvtHandler
{
public:
    wxTaskBarIcon(wxPyTaskBarIconType iconType=wxTBI_DEFAULT)
    { wxPyRaiseNotImplemented(); }
};


class wxTaskBarIconEvent : public wxEvent
{
public:
    wxTaskBarIconEvent(wxEventType, wxTaskBarIcon *)
        { wxPyRaiseNotImplemented(); }
    virtual wxEvent* Clone() const { return NULL; }
    bool IsOk() const { return false; }
    bool IsIconInstalled() const { return false; }
    bool SetIcon(const wxIcon& icon, const wxString& tooltip = wxPyEmptyString) { return false; }
    bool RemoveIcon() { return false; }
    bool PopupMenu(wxMenu *menu) { return false; }
#ifdef __WXMSW__
    bool ShowBalloon(const wxString& title,
                     const wxString& text,
                     unsigned msec = 0, 
                     int flags = 0)   { return false; }
#endif  
    static bool IsAvailable() { return false; };
};

enum {
    wxEVT_TASKBAR_MOVE = 0,
    wxEVT_TASKBAR_LEFT_DOWN = 0,
    wxEVT_TASKBAR_LEFT_UP = 0,
    wxEVT_TASKBAR_RIGHT_DOWN = 0,
    wxEVT_TASKBAR_RIGHT_UP = 0,
    wxEVT_TASKBAR_LEFT_DCLICK = 0,
    wxEVT_TASKBAR_RIGHT_DCLICK = 0,
};


#else
// Otherwise make a class that can virtualize CreatePopupMenu
class wxPyTaskBarIcon : public wxTaskBarIcon
{
    DECLARE_ABSTRACT_CLASS(wxPyTaskBarIcon)
public:
    wxPyTaskBarIcon(wxPyTaskBarIconType iconType=wxTBI_DEFAULT) :
#ifdef __WXOSX_COCOA__
        wxTaskBarIcon((wxTaskBarIconType)iconType) {}
#else
        wxTaskBarIcon() {}
#endif
    
    wxMenu* CreatePopupMenu() {
        wxMenu *rval = NULL;
        bool found;
        wxPyBlock_t blocked = wxPyBeginBlockThreads();
        if ((found = wxPyCBH_findCallback(m_myInst, "CreatePopupMenu"))) {
            PyObject* ro;
            wxMenu* ptr;
            ro = wxPyCBH_callCallbackObj(m_myInst, Py_BuildValue("()"));
            if (ro) {
                if (wxPyConvertSwigPtr(ro, (void **)&ptr, wxT("wxMenu")))
                    rval = ptr;
                Py_DECREF(ro);
            }
        }
        wxPyEndBlockThreads(blocked);
        if (! found)
            rval = wxTaskBarIcon::CreatePopupMenu();
        return rval;
    }

    PYPRIVATE;
};

IMPLEMENT_ABSTRACT_CLASS(wxPyTaskBarIcon, wxTaskBarIcon);

#endif
%}


enum wxPyTaskBarIconType
{
    wxTBI_DOCK,
    wxTBI_CUSTOM_STATUS_ITEM,
    wxTBI_DEFAULT = wxTBI_CUSTOM_STATUS_ITEM
};


MustHaveApp(wxPyTaskBarIcon);

%rename(TaskBarIcon) wxPyTaskBarIcon;
class wxPyTaskBarIcon : public wxEvtHandler
{
public:
    %pythonAppend wxPyTaskBarIcon   "self._setOORInfo(self);" setCallbackInfo(TaskBarIcon)

    wxPyTaskBarIcon(wxPyTaskBarIconType iconType=wxTBI_DEFAULT);
    ~wxPyTaskBarIcon();

    void _setCallbackInfo(PyObject* self, PyObject* _class, int incref=0);

    void Destroy();
    
    bool IsOk() const;
    %pythoncode { def __nonzero__(self): return self.IsOk() }

    bool IsIconInstalled() const;

    bool SetIcon(const wxIcon& icon, const wxString& tooltip = wxPyEmptyString);
    bool RemoveIcon();
    bool PopupMenu(wxMenu *menu);

    DocStr(ShowBalloon,
           "Show a balloon notification (the icon must have been already
initialized using SetIcon).  Only implemented for Windows.

title and text are limited to 63 and 255 characters respectively, msec
is the timeout, in milliseconds, before the balloon disappears (will
be clamped down to the allowed 10-30s range by Windows if it's outside
it) and flags can include wxICON_ERROR/INFO/WARNING to show a
corresponding icon

Returns True if balloon was shown, False on error (incorrect parameters
or function unsupported by OS)
", "");
#ifdef __WXMSW__
    bool ShowBalloon(const wxString& title,
                     const wxString& text,
                     unsigned msec = 0,
                     int flags = 0);

#else
    %extend {
        bool ShowBalloon(const wxString& title,
                         const wxString& text,
                         unsigned msec = 0,
                         int flags = 0)  { return false; }
    }
#endif

    static bool IsAvailable();
};



class wxTaskBarIconEvent : public wxEvent
{
public:
    wxTaskBarIconEvent(wxEventType evtType, wxTaskBarIcon *tbIcon);
};



%constant wxEventType wxEVT_TASKBAR_MOVE;
%constant wxEventType wxEVT_TASKBAR_LEFT_DOWN;
%constant wxEventType wxEVT_TASKBAR_LEFT_UP;
%constant wxEventType wxEVT_TASKBAR_RIGHT_DOWN;
%constant wxEventType wxEVT_TASKBAR_RIGHT_UP;
%constant wxEventType wxEVT_TASKBAR_LEFT_DCLICK;
%constant wxEventType wxEVT_TASKBAR_RIGHT_DCLICK;
%constant wxEventType wxEVT_TASKBAR_CLICK;
%constant wxEventType wxEVT_TASKBAR_BALLOON_TIMEOUT;
%constant wxEventType wxEVT_TASKBAR_BALLOON_CLICK;


%pythoncode {
EVT_TASKBAR_MOVE = wx.PyEventBinder (         wxEVT_TASKBAR_MOVE )
EVT_TASKBAR_LEFT_DOWN = wx.PyEventBinder (    wxEVT_TASKBAR_LEFT_DOWN )
EVT_TASKBAR_LEFT_UP = wx.PyEventBinder (      wxEVT_TASKBAR_LEFT_UP )
EVT_TASKBAR_RIGHT_DOWN = wx.PyEventBinder (   wxEVT_TASKBAR_RIGHT_DOWN )
EVT_TASKBAR_RIGHT_UP = wx.PyEventBinder (     wxEVT_TASKBAR_RIGHT_UP )
EVT_TASKBAR_LEFT_DCLICK = wx.PyEventBinder (  wxEVT_TASKBAR_LEFT_DCLICK )
EVT_TASKBAR_RIGHT_DCLICK = wx.PyEventBinder ( wxEVT_TASKBAR_RIGHT_DCLICK )
EVT_TASKBAR_CLICK =  wx.PyEventBinder (       wxEVT_TASKBAR_CLICK )
EVT_TASKBAR_BALLOON_TIMEOUT = wx.PyEventBinder ( wxEVT_TASKBAR_BALLOON_TIMEOUT )
EVT_TASKBAR_BALLOON_CLICK = wx.PyEventBinder ( wxEVT_TASKBAR_BALLOON_CLICK )
}

//---------------------------------------------------------------------------
