/////////////////////////////////////////////////////////////////////////////
// Name:        xh_stbox.h
// Purpose:     XML resource handler for wxStaticBox
// Author:      Brian Gavin
// Created:     2000/09/00
// RCS-ID:      $Id: xh_stbox.h,v 1.2.2.1 2005/06/20 17:33:54 MR Exp $
// Copyright:   (c) 2000 Brian Gavin
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_XH_STBOX_H_
#define _WX_XH_STBOX_H_

#include "wx/xrc/xmlres.h"


class WXXMLDLLEXPORT wxStaticBoxXmlHandler : public wxXmlResourceHandler
{
public:
    wxStaticBoxXmlHandler();
    virtual wxObject *DoCreateResource();
    virtual bool CanHandle(wxXmlNode *node);
};


#endif // _WX_XH_STBOX_H_
