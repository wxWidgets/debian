/////////////////////////////////////////////////////////////////////////////
// Name:        icon.cpp
// Purpose:
// Author:      Robert Roebling
// Id:          $Id: icon.cpp,v 1.7 1998/12/09 17:29:48 VZ Exp $
// Copyright:   (c) 1998 Robert Roebling
// Licence:   	wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifdef __GNUG__
#pragma implementation "icon.h"
#endif

#include "wx/icon.h"

//-----------------------------------------------------------------------------
// wxIcon
//-----------------------------------------------------------------------------

IMPLEMENT_DYNAMIC_CLASS(wxIcon,wxBitmap)

wxIcon::wxIcon( const char **bits, int WXUNUSED(width), int WXUNUSED(height) ) :
    wxBitmap( bits )
{
}

wxIcon::wxIcon( char **bits, int WXUNUSED(width), int WXUNUSED(height) ) :
    wxBitmap( bits )
{
}

wxIcon::wxIcon() :  wxBitmap()
{
}

wxIcon::wxIcon( const wxIcon& icon ) : wxBitmap()
{
    Ref(icon);
}

wxIcon& wxIcon::operator = ( const wxIcon& icon )
{
    if (*this == icon) return (*this);
    Ref(icon);
    return *this;
}

