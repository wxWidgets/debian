/////////////////////////////////////////////////////////////////////////////
// Name:        xh_gauge.h
// Purpose:     XML resource handler for wxGauge
// Author:      Bob Mitchell
// Created:     2000/03/21
// RCS-ID:      $Id: xh_gauge.h,v 1.2.2.1 2005/06/20 17:33:49 MR Exp $
// Copyright:   (c) 2000 Bob Mitchell and Verant Interactive
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_XH_GAUGE_H_
#define _WX_XH_GAUGE_H_

#include "wx/defs.h"

#if wxUSE_GAUGE

#include "wx/xrc/xmlres.h"


class WXXMLDLLEXPORT wxGaugeXmlHandler : public wxXmlResourceHandler
{
    enum
    {
        wxGAUGE_DEFAULT_RANGE = 100
    };

public:
    wxGaugeXmlHandler();
    virtual wxObject *DoCreateResource();
    virtual bool CanHandle(wxXmlNode *node);
};

#endif

#endif // _WX_XH_GAUGE_H_
