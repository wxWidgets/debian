/////////////////////////////////////////////////////////////////////////////
// Name:        statline.h
// Purpose:
// Author:      Robert Roebling
// Id:          $Id: statline.h,v 1.6.2.1 2005/06/20 17:37:05 MR Exp $
// Copyright:   (c) 1998 Robert Roebling
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////


#ifndef __GTKSTATICLINEH__
#define __GTKSTATICLINEH__

#include "wx/defs.h"

#if wxUSE_STATLINE

#include "wx/object.h"
#include "wx/list.h"
#include "wx/control.h"

//-----------------------------------------------------------------------------
// classes
//-----------------------------------------------------------------------------

class wxStaticLine;

//-----------------------------------------------------------------------------
// wxStaticLine
//-----------------------------------------------------------------------------

class wxStaticLine : public wxStaticLineBase
{
    DECLARE_DYNAMIC_CLASS(wxStaticLine)

public:
    wxStaticLine();
    wxStaticLine( wxWindow *parent, wxWindowID id,
            const wxPoint &pos = wxDefaultPosition, const wxSize &size = wxDefaultSize, 
            long style = wxLI_HORIZONTAL, const wxString &name = wxStaticTextNameStr );
    bool Create(  wxWindow *parent, wxWindowID id,
            const wxPoint &pos = wxDefaultPosition, const wxSize &size = wxDefaultSize, 
            long style = wxLI_HORIZONTAL, const wxString &name = wxStaticTextNameStr );
};

#endif 
  // wxUSE_STATLINE
  
#endif 
  // __GTKSTATICLINEH__
