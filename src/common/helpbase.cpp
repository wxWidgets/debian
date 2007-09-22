/////////////////////////////////////////////////////////////////////////////
// Name:        helpbase.cpp
// Purpose:     Help system base classes
// Author:      Julian Smart
// Modified by:
// Created:     04/01/98
// RCS-ID:      $Id: helpbase.cpp,v 1.3 1999/12/14 23:42:34 VS Exp $
// Copyright:   (c) Julian Smart and Markus Holzem
// Licence:   	wxWindows license
/////////////////////////////////////////////////////////////////////////////

#ifdef __GNUG__
#pragma implementation "helpbase.h"
#endif

// For compilers that support precompilation, includes "wx.h".
#include "wx/wxprec.h"

#ifdef __BORLANDC__
#pragma hdrstop
#endif

#ifndef WX_PRECOMP
#include "wx/defs.h"
#endif

#include "wx/helpbase.h"

#if wxUSE_HELP

IMPLEMENT_CLASS(wxHelpControllerBase, wxObject)

#endif // wxUSE_HELP
