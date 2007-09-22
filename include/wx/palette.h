/////////////////////////////////////////////////////////////////////////////
// Name:        wx/palette.h
// Purpose:     Common header and base class for wxPalette
// Author:      Julian Smart
// Modified by:
// Created:
// RCS-ID:      $Id: palette.h,v 1.11.2.1 2005/05/04 18:23:29 JS Exp $
// Copyright:   (c) Julian Smart
// Licence:     wxWindows Licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_PALETTE_H_BASE_
#define _WX_PALETTE_H_BASE_

// include it to get wxUSE_PALETTE value
#include "wx/setup.h"

#if wxUSE_PALETTE

#if defined(__WXMSW__)
    #include "wx/msw/palette.h"
#elif defined(__WXMOTIF__)
    #include "wx/motif/palette.h"
#elif defined(__WXGTK__)
    #include "wx/generic/paletteg.h"
#elif defined(__WXX11__)
    #include "wx/x11/palette.h"
#elif defined(__WXMGL__)
    #include "wx/mgl/palette.h"
#elif defined(__WXMAC__)
    #include "wx/mac/palette.h"
#elif defined(__WXPM__)
    #include "wx/os2/palette.h"
#elif defined(__WXSTUBS__)
    #include "wx/stubs/palette.h"
#endif

#endif // wxUSE_PALETTE

#endif
    // _WX_PALETTE_H_BASE_
