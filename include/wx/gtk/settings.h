/////////////////////////////////////////////////////////////////////////////
// Name:        settings.h
// Purpose:
// Author:      Robert Roebling
// Id:          $Id: settings.h,v 1.4 1998/12/12 16:41:43 RR Exp $
// Copyright:   (c) 1998 Robert Roebling
// Licence:   	wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef __GTKSETTINGSH__
#define __GTKSETTINGSH__

#ifdef __GNUG__
#pragma interface
#endif

#include "wx/defs.h"
#include "wx/gdicmn.h"
#include "wx/pen.h"
#include "wx/font.h"

class wxSystemSettings: public wxObject
{
public:
    inline wxSystemSettings() {}

    inline static void Init() {}
    static void Done();

    // Get a system colour
    static wxColour    GetSystemColour(int index);

    // Get a system font
    static wxFont      GetSystemFont(int index);

    // Get a system metric, e.g. scrollbar size
    static int         GetSystemMetric(int index);
};

#endif
    // __GTKSETTINGSH__
