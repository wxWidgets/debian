/////////////////////////////////////////////////////////////////////////////
// Name:        _functions.i
// Purpose:     SWIG interface defs for various functions and such
//
// Author:      Robin Dunn
//
// Created:     3-July-1997
// RCS-ID:      $Id: _functions.i 63597 2010-03-01 23:39:58Z RD $
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module


%{
#include <wx/stockitem.h>
#include <wx/thread.h>
%}

//---------------------------------------------------------------------------

MAKE_CONST_WXSTRING(FileSelectorPromptStr);
MAKE_CONST_WXSTRING(FileSelectorDefaultWildcardStr);
MAKE_CONST_WXSTRING(DirSelectorPromptStr);

//---------------------------------------------------------------------------
%newgroup;


long wxNewId();
void wxRegisterId(long id);
long wxGetCurrentId();

// Returns true if the ID is in the list of recognized stock actions
bool wxIsStockID(wxWindowID id);
 
// Returns true of the label is empty or label of a stock button with
// given ID
bool wxIsStockLabel(wxWindowID id, const wxString& label);

enum wxStockLabelQueryFlag
{
    wxSTOCK_NOFLAGS,

    wxSTOCK_WITH_MNEMONIC,
    wxSTOCK_WITH_ACCELERATOR,

    // by default, stock items text is returned with ellipsis, if appropriate,
    // this flag allows to avoid having it
    wxSTOCK_WITHOUT_ELLIPSIS,

    // return label for button, not menu item: buttons should always use
    // mnemonics and never use ellipsis
    wxSTOCK_FOR_BUTTON,
};


// Returns label that should be used for given stock UI element (e.g. "&OK"
// for wxID_OK):
wxString wxGetStockLabel(wxWindowID id,
                         long flags = wxSTOCK_WITH_MNEMONIC);


enum wxStockHelpStringClient
{
    wxSTOCK_MENU        // help string to use for menu items
};

// Returns an help string for the given stock UI element and for the given "context".
wxString wxGetStockHelpString(wxWindowID id,
                              wxStockHelpStringClient client = wxSTOCK_MENU);




MustHaveApp(wxBell);
void wxBell();

MustHaveApp(wxEndBusyCursor);
void wxEndBusyCursor();

bool wxIsBusy();
wxString wxNow();
bool wxShell(const wxString& command = wxPyEmptyString);


DocDeclA(
    int, wxGetOsVersion(int *OUTPUT, int *OUTPUT),
    "GetOsVersion() -> (platform, major, minor)");

wxString wxGetOsDescription();


// Get platform endianness
bool wxIsPlatformLittleEndian();

// Get platform architecture
bool wxIsPlatform64Bit();


// TODO:
// // Parses the wildCard, returning the number of filters.
// // Returns 0 if none or if there's a problem,
// // The arrays will contain an equal number of items found before the error.
// // wildCard is in the form:
// // "All files (*)|*|Image Files (*.jpeg *.png)|*.jpg;*.png"
// int wxParseCommonDialogsFilter(const wxString& wildCard, wxArrayString& descriptions, wxArrayString& filters);


%typemap(out) wxMemorySize {
    %#if wxUSE_LONGLONG
         $result = PyLong_FromLongLong($1.GetValue());
    %#else
         $result = PyInt_FromLong($1);
    %#endif
}

#if defined(__WXMSW__) || defined(__WXMAC__)
wxMemorySize wxGetFreeMemory();
#else
%inline %{
    wxMemorySize wxGetFreeMemory()
        { wxPyRaiseNotImplemented(); return 0; }
%}
#endif

enum wxShutdownFlags
{
    wxSHUTDOWN_FORCE    = 1,// can be combined with other flags (MSW-only)
    wxSHUTDOWN_POWEROFF = 2,// power off the computer
    wxSHUTDOWN_REBOOT   = 4,// shutdown and reboot
    wxSHUTDOWN_LOGOFF   = 8 // close session (currently MSW-only)
};

// Shutdown or reboot the PC
MustHaveApp(wxShutdown);
bool wxShutdown(wxShutdownFlags wFlags);


void wxSleep(int secs);
void wxMilliSleep(unsigned long milliseconds);
void wxMicroSleep(unsigned long microseconds);
%pythoncode { Usleep = MilliSleep }

void wxEnableTopLevelWindows(bool enable);

wxString wxStripMenuCodes(const wxString& in);


wxString wxGetEmailAddress();
wxString wxGetHostName();
wxString wxGetFullHostName();
wxString wxGetUserId();
wxString wxGetUserName();
wxString wxGetHomeDir();
wxString wxGetUserHome(const wxString& user = wxPyEmptyString);

unsigned long wxGetProcessId();

void wxTrap();


// Dialog Functions

MustHaveApp(wxFileSelector);
wxString wxFileSelector(const wxString& message = wxPyFileSelectorPromptStr,
                        const wxString& default_path = wxPyEmptyString,
                        const wxString& default_filename = wxPyEmptyString,
                        const wxString& default_extension = wxPyEmptyString,
                        const wxString& wildcard = wxPyFileSelectorDefaultWildcardStr,
                        int flags = 0,
                        wxWindow *parent = NULL,
                        int x = -1, int y = -1);

// TODO: wxFileSelectorEx


// Ask for filename to load
MustHaveApp(wxLoadFileSelector);
wxString wxLoadFileSelector(const wxString& what,
                            const wxString& extension,
                            const wxString& default_name = wxPyEmptyString,
                            wxWindow *parent = NULL);

// Ask for filename to save
MustHaveApp(wxSaveFileSelector);
wxString wxSaveFileSelector(const wxString& what,
                            const wxString& extension,
                            const wxString& default_name = wxPyEmptyString,
                            wxWindow *parent = NULL);


MustHaveApp(wxDirSelector);
wxString wxDirSelector(const wxString& message = wxPyDirSelectorPromptStr,
                       const wxString& defaultPath = wxPyEmptyString,
                       long style = wxDD_DEFAULT_STYLE,
                       const wxPoint& pos = wxDefaultPosition,
                       wxWindow *parent = NULL);

MustHaveApp(wxGetTextFromUser);
wxString wxGetTextFromUser(const wxString& message,
                           const wxString& caption = wxPyEmptyString,
                           const wxString& default_value = wxPyEmptyString,
                           wxWindow *parent = NULL,
                           int x = -1, int y = -1,
                           bool centre = true);

MustHaveApp(wxGetPasswordFromUser);
wxString wxGetPasswordFromUser(const wxString& message,
                               const wxString& caption = wxPyEmptyString,
                               const wxString& default_value = wxPyEmptyString,
                               wxWindow *parent = NULL);


// TODO: Need to custom wrap this one...
// int wxGetMultipleChoice(char* message, char* caption,
//                         int LCOUNT, char** choices,
//                         int nsel, int *selection,
//                         wxWindow *parent = NULL, int x = -1, int y = -1,
//                         bool centre = true, int width=150, int height=200);


MustHaveApp(wxGetSingleChoice);
wxString wxGetSingleChoice(const wxString& message, const wxString& caption,
                           int choices, wxString* choices_array,
                           wxWindow *parent = NULL,
                           int x = -1, int y = -1,
                           bool centre = true,
                           int width=150, int height=200);

MustHaveApp(wxGetSingleChoiceIndex);
int wxGetSingleChoiceIndex(const wxString& message, const wxString& caption,
                           int choices, wxString* choices_array,
                           wxWindow *parent = NULL,
                           int x = -1, int y = -1,
                           bool centre = true,
                           int width=150, int height=200);


MustHaveApp(wxMessageBox);
int wxMessageBox(const wxString& message,
                 const wxString& caption = wxPyEmptyString,
                 int style = wxOK | wxCENTRE,
                 wxWindow *parent = NULL,
                 int x = -1, int y = -1);

MustHaveApp(wxGetNumberFromUser);
long wxGetNumberFromUser(const wxString& message,
                         const wxString& prompt,
                         const wxString& caption,
                         long value,
                         long min = 0, long max = 100,
                         wxWindow *parent = NULL,
                         const wxPoint& pos = wxDefaultPosition);

// GDI Functions

MustHaveApp(wxColourDisplay);
bool wxColourDisplay();

MustHaveApp(wxDisplayDepth);
int wxDisplayDepth();

MustHaveApp(wxGetDisplayDepth);
int wxGetDisplayDepth();

MustHaveApp(wxDisplaySize);
DocDeclA(
    void, wxDisplaySize(int* OUTPUT, int* OUTPUT),
    "DisplaySize() -> (width, height)");

MustHaveApp(wxGetDisplaySize);
wxSize wxGetDisplaySize();

MustHaveApp(wxDisplaySizeMM);
DocDeclA(
    void, wxDisplaySizeMM(int* OUTPUT, int* OUTPUT),
    "DisplaySizeMM() -> (width, height)");

MustHaveApp(wxGetDisplaySizeMM);
wxSize wxGetDisplaySizeMM();

MustHaveApp(wxGetDisplayPPI);
wxSize wxGetDisplayPPI();

MustHaveApp(wxClientDisplayRect);
DocDeclA(
    void, wxClientDisplayRect(int *OUTPUT, int *OUTPUT, int *OUTPUT, int *OUTPUT),
    "ClientDisplayRect() -> (x, y, width, height)");

MustHaveApp(wxGetClientDisplayRect);
wxRect wxGetClientDisplayRect();


MustHaveApp(wxSetCursor);
void wxSetCursor(wxCursor& cursor);


MustHaveApp(wxGetXDisplay);
DocStr(wxGetXDisplay,
"Returns a swigified pointer to the X11 display.  Returns None on
other platforms.", "");
%inline %{
    void* wxGetXDisplay()
    {
#ifdef __WXGTK__
        return wxGetDisplay();
#else
        return NULL;
#endif
    }
%}


// Miscellaneous functions

MustHaveApp(wxBeginBusyCursor);
void wxBeginBusyCursor(wxCursor *cursor = wxHOURGLASS_CURSOR);


MustHaveApp(wxGetMousePosition);
DocDeclStr(
    wxPoint, wxGetMousePosition(),
    "Get the current mouse position on the screen.", "");

MustHaveApp(FindWindowAtPointer);
DocStr(FindWindowAtPointer,
       "Returns the window currently under the mouse pointer, if it belongs to
    this application.  Otherwise it returns None.", "");
%inline %{
    wxWindow* FindWindowAtPointer() {
        wxPoint unused;
        return wxFindWindowAtPointer(unused);
    }
%}
 

MustHaveApp(wxGetActiveWindow);
DocDeclStr(
    wxWindow *, wxGetActiveWindow(),
    "Get the currently active window of this application, or None", "");


MustHaveApp(wxGenericFindWindowAtPoint);
wxWindow* wxGenericFindWindowAtPoint(const wxPoint& pt);

MustHaveApp(wxFindWindowAtPoint);
wxWindow* wxFindWindowAtPoint(const wxPoint& pt);

MustHaveApp(wxGetTopLevelParent);
wxWindow* wxGetTopLevelParent(wxWindow *win);


// flags for wxLaunchDefaultBrowser
enum
{
    wxBROWSER_NEW_WINDOW,
    wxBROWSER_NOBUSYCURSOR
};

DocDeclStr(
    bool , wxLaunchDefaultBrowser(const wxString& url, int flags = 0),
    "Launches the user's default browser and tells it to open the location
at ``url``.  Returns ``True`` if the application was successfully
launched.", "");


DocDeclStr(
    bool , wxLaunchDefaultApplication(const wxString& path, int flags = 0),
    "Launch document in the user's default application.", "");



MustHaveApp(wxGetKeyState);
DocDeclStr(
    bool , wxGetKeyState(wxKeyCode key),
    "Get the state of a key (true if pressed or toggled on, false if not.)
This is generally most useful getting the state of the modifier or
toggle keys.  On some platforms those may be the only keys that this
function is able to detect.
", "");


//---------------------------------------------------------------------------

MustHaveApp(wxWakeUpMainThread);

#if defined(__WXMSW__)
void wxWakeUpMainThread();
#else
%inline %{
    void wxWakeUpMainThread() {}
%}
#endif


MustHaveApp(wxMutexGuiEnter);
void wxMutexGuiEnter();

MustHaveApp(wxMutexGuiLeave);
void wxMutexGuiLeave();


MustHaveApp(wxMutexGuiLocker);
class wxMutexGuiLocker  {
public:
    wxMutexGuiLocker();
    ~wxMutexGuiLocker();
};


MustHaveApp(wxThread_IsMain);
%inline %{
    bool wxThread_IsMain() {
#ifdef WXP_WITH_THREAD
        return wxThread::IsMain();
#else
        return true;
#endif
    }
%}

//---------------------------------------------------------------------------
//---------------------------------------------------------------------------
