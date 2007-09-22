/////////////////////////////////////////////////////////////////////////////
// Name:        xh_choic.h
// Purpose:     XML resource handler for wxChoice
// Author:      Bob Mitchell
// Created:     2000/03/21
// RCS-ID:      $Id: xh_choic.h,v 1.2.2.1 2005/06/20 17:33:48 MR Exp $
// Copyright:   (c) 2000 Bob Mitchell and Verant Interactive
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_XH_CHOIC_H_
#define _WX_XH_CHOIC_H_

#include "wx/xrc/xmlres.h"

class WXXMLDLLEXPORT wxChoiceXmlHandler : public wxXmlResourceHandler
{
public:
    wxChoiceXmlHandler();
    virtual wxObject *DoCreateResource();
    virtual bool CanHandle(wxXmlNode *node);
private:
    bool m_insideBox;
    wxArrayString strList;
};


#endif // _WX_XH_CHOIC_H_
