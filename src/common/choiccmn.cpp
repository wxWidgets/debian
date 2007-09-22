/////////////////////////////////////////////////////////////////////////////
// Name:        common/choiccmn.cpp
// Purpose:     common (to all ports) wxChoice functions
// Author:      Vadim Zeitlin
// Modified by:
// Created:     26.07.99
// RCS-ID:      $Id: choiccmn.cpp,v 1.8.2.1 2005/06/20 17:40:37 MR Exp $
// Copyright:   (c) wxWindows team
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// ============================================================================
// declarations
// ============================================================================

// ----------------------------------------------------------------------------
// headers
// ----------------------------------------------------------------------------

// For compilers that support precompilation, includes "wx.h".
#include "wx/wxprec.h"

#ifdef __BORLANDC__
    #pragma hdrstop
#endif

#if wxUSE_CHOICE

#ifndef WX_PRECOMP
    #include "wx/choice.h"
#endif

// ============================================================================
// implementation
// ============================================================================

wxChoiceBase::~wxChoiceBase()
{
    // this destructor is required for Darwin
}

// ----------------------------------------------------------------------------
// selection
// ----------------------------------------------------------------------------

bool wxChoiceBase::SetStringSelection(const wxString& s)
{
    int sel = FindString(s);
    wxCHECK_MSG( sel != -1, FALSE,
                 wxT("invalid string in wxChoice::SetStringSelection") );

    Select(sel);

    return TRUE;
}

// ----------------------------------------------------------------------------
// misc
// ----------------------------------------------------------------------------

void wxChoiceBase::Command(wxCommandEvent& event)
{
    SetSelection(event.m_commandInt);
    (void)ProcessEvent(event);
}

#endif // wxUSE_CHOICE

