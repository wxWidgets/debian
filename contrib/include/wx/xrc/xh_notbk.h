/////////////////////////////////////////////////////////////////////////////
// Name:        xh_notbk.h
// Purpose:     XML resource handler for wxNotebook
// Author:      Vaclav Slavik
// RCS-ID:      $Id: xh_notbk.h,v 1.2.2.1 2005/06/20 17:33:51 MR Exp $
// Copyright:   (c) 2000 Vaclav Slavik
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_XH_NOTBK_H_
#define _WX_XH_NOTBK_H_

#include "wx/xrc/xmlres.h"

#if wxUSE_NOTEBOOK

class WXDLLEXPORT wxNotebook;

class WXXMLDLLEXPORT wxNotebookXmlHandler : public wxXmlResourceHandler
{
public:
    wxNotebookXmlHandler();
    virtual wxObject *DoCreateResource();
    virtual bool CanHandle(wxXmlNode *node);

private:
    bool m_isInside;
    wxNotebook *m_notebook;
};

#endif

#endif // _WX_XH_NOTBK_H_
