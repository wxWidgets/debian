/////////////////////////////////////////////////////////////////////////////
// Name:        xh_radbt.h
// Purpose:     XML resource handler for radio buttons
// Author:      Bob Mitchell
// Created:     2000/03/21
// RCS-ID:      $Id: xh_radbt.h,v 1.2.2.1 2005/06/20 17:33:52 MR Exp $
// Copyright:   (c) 2000 Bob Mitchell and Verant Interactive
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_XH_RADBT_H_
#define _WX_XH_RADBT_H_

#include "wx/xrc/xmlres.h"
#include "wx/defs.h"

#if wxUSE_RADIOBOX

class WXXMLDLLEXPORT wxRadioButtonXmlHandler : public wxXmlResourceHandler
{
public:
    wxRadioButtonXmlHandler();
    virtual wxObject *DoCreateResource();
    virtual bool CanHandle(wxXmlNode *node);
};

#endif

#endif // _WX_XH_RADIOBUTTON_H_
