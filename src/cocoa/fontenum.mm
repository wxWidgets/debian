/////////////////////////////////////////////////////////////////////////////
// Name:        src/cocoa/fontenum.mm
// Purpose:     wxFontEnumerator class for Cocoa
// Author:      David Elliott
// Modified by:
// Created:     2003/07/23
// RCS-ID:      $Id: fontenum.mm 64940 2010-07-13 13:29:13Z VZ $
// Copyright:   (c) David Elliott
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#include "wx/wxprec.h"
#ifndef WX_PRECOMP
#endif

#include "wx/fontenum.h"

bool wxFontEnumerator::EnumerateFacenames(wxFontEncoding encoding,
                                          bool fixedWidthOnly)
{
    return false;
}

bool wxFontEnumerator::EnumerateEncodings(const wxString& family)
{
    return false;
}

