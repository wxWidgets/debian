/////////////////////////////////////////////////////////////////////////////
// Name:        webviewarchivehandler.h
// Purpose:     interface of wxWebViewArchiveHandler
// Author:      wxWidgets team
// RCS-ID:      $Id: webviewarchivehandler.h 69049 2011-09-10 18:09:12Z SJL $
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

/**
    @class wxWebViewArchiveHandler
  
    A custom handler for the file scheme which also supports loading from 
    archives. The syntax for wxWebViewArchiveHandler differs from virtual file 
    systems in the rest of wxWidgets by using a syntax such as
    <code> scheme:///C:/exmaple/docs.zip;protocol=zip/main.htm </code> 
    Currently the only supported protocol is @c zip. 
   
    @since 2.9.3
    @library{wxwebview}
    @category{webview}
    
    @see wxWebView, wxWebViewHandler
 */
class wxWebViewArchiveHandler : public wxWebViewHandler
{
public:
    /**
        Constructor.
    */
    wxWebViewArchiveHandler(const wxString& scheme);
    virtual wxFSFile* GetFile(const wxString &uri);
};