/////////////////////////////////////////////////////////////////////////////
// Name:        wx/msw/settings.h
// Purpose:     wxSystemSettings class
// Author:      Julian Smart
// Modified by:
// Created:     01/02/97
// RCS-ID:      $Id: settings.h,v 1.4.2.1 2001/04/21 15:54:19 VZ Exp $
// Copyright:   (c) Julian Smart
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_SETTINGS_H_
#define _WX_SETTINGS_H_

#ifdef __GNUG__
#pragma interface "settings.h"
#endif

#include "wx/colour.h"
#include "wx/font.h"

class WXDLLEXPORT wxSystemSettings : public wxObject
{
public:
    wxSystemSettings() { }

    // Get a system colour
    static wxColour GetSystemColour(int index);

    // Get a system font
    static wxFont GetSystemFont(int index);

    // Get a system metric, e.g. scrollbar size
    static int GetSystemMetric(int index);
};

#endif
    // _WX_SETTINGS_H_
