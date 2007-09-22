/////////////////////////////////////////////////////////////////////////////
// Name:        xh_chckl.h
// Purpose:     XML resource handler for wxCheckListBox
// Author:      Bob Mitchell
// Created:     2000/03/21
// RCS-ID:      $Id: xh_chckl.h,v 1.2.2.1 2003/08/28 09:35:44 VS Exp $
// Copyright:   (c) 2000 Bob Mitchell and Verant Interactive
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_XH_CHCKL_H_
#define _WX_XH_CHCKL_H_

#if defined(__GNUG__) && !defined(__APPLE__)
#pragma interface "xh_chckl.h"
#endif

#include "wx/xrc/xmlres.h"

class WXXMLDLLEXPORT wxCheckListBoxXmlHandler : public wxXmlResourceHandler
{
public:
    wxCheckListBoxXmlHandler();
    virtual wxObject *DoCreateResource();
    virtual bool CanHandle(wxXmlNode *node);
private:
    bool m_insideBox;
    wxArrayString strList;
};



#endif // _WX_XH_CHECKLIST_H_
