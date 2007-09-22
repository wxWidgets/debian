/////////////////////////////////////////////////////////////////////////////
// Name:        xh_bmp.cpp
// Purpose:     XRC resource for wxBitmap and wxIcon
// Author:      Vaclav Slavik
// Created:     2000/09/09
// RCS-ID:      $Id: xh_bmp.cpp,v 1.8 2004/09/23 09:18:10 VS Exp $
// Copyright:   (c) 2000 Vaclav Slavik
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifdef __GNUG__
#pragma implementation "xh_bmp.h"
#endif

// For compilers that support precompilation, includes "wx.h".
#include "wx/wxprec.h"

#ifdef __BORLANDC__
    #pragma hdrstop
#endif

#if wxUSE_XRC

#include "wx/xrc/xh_bmp.h"
#include "wx/bitmap.h"

IMPLEMENT_DYNAMIC_CLASS(wxBitmapXmlHandler, wxXmlResourceHandler)

wxBitmapXmlHandler::wxBitmapXmlHandler()
: wxXmlResourceHandler()
{
}

wxObject *wxBitmapXmlHandler::DoCreateResource()
{
    return new wxBitmap(GetBitmap(wxT("")));
}

bool wxBitmapXmlHandler::CanHandle(wxXmlNode *node)
{
    return IsOfClass(node, wxT("wxBitmap"));
}

IMPLEMENT_DYNAMIC_CLASS(wxIconXmlHandler, wxXmlResourceHandler)

wxIconXmlHandler::wxIconXmlHandler()
: wxXmlResourceHandler()
{
}

wxObject *wxIconXmlHandler::DoCreateResource()
{
    return new wxIcon(GetIcon(wxT("")));
}

bool wxIconXmlHandler::CanHandle(wxXmlNode *node)
{
    return IsOfClass(node, wxT("wxIcon"));
}

#endif // wxUSE_XRC
