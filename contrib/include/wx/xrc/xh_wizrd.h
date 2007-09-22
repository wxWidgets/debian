/////////////////////////////////////////////////////////////////////////////
// Name:        xh_wizrd.h
// Purpose:     XML resource handler for wxWizard
// Author:      Vaclav Slavik
// Created:     2003/03/02
// RCS-ID:      $Id: xh_wizrd.h,v 1.1.2.1 2003/05/25 13:20:23 JS Exp $
// Copyright:   (c) 2000 Vaclav Slavik
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_XH_WIZRD_H_
#define _WX_XH_WIZRDL_H_

#if defined(__GNUG__) && !defined(__APPLE__)
#pragma interface "xh_wizrd.h"
#endif

#include "wx/xrc/xmlres.h"

#if wxUSE_WIZARDDLG

#include "wx/wizard.h"

class WXXMLDLLEXPORT wxWizardXmlHandler : public wxXmlResourceHandler
{
public:
    wxWizardXmlHandler();
    virtual wxObject *DoCreateResource();
    virtual bool CanHandle(wxXmlNode *node);

private:
    wxWizard *m_wizard;
    wxWizardPageSimple *m_lastSimplePage;
};

#endif

#endif // _WX_XH_PANEL_H_
