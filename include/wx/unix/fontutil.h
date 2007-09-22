/////////////////////////////////////////////////////////////////////////////
// Name:        wx/unix/fontutil.h
// Purpose:     font-related helper functions for Unix/X11
// Author:      Vadim Zeitlin
// Modified by:
// Created:     05.11.99
// RCS-ID:      $Id: fontutil.h,v 1.3 1999/11/08 15:59:33 VZ Exp $
// Copyright:   (c) wxWindows team
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_UNIX_FONTUTIL_H_
#define _WX_UNIX_FONTUTIL_H_

#ifdef __X__
    typedef WXFontStructPtr wxNativeFont;
#elif defined(__WXGTK__)
    typedef GdkFont *wxNativeFont;
#else
    #error "Unsupported toolkit"
#endif

// returns the handle of the nearest available font or 0
extern wxNativeFont wxLoadQueryNearestFont(int pointSize,
                                           int family,
                                           int style,
                                           int weight,
                                           bool underlined,
                                           const wxString &facename,
                                           wxFontEncoding encoding);

#endif // _WX_UNIX_FONTUTIL_H_
