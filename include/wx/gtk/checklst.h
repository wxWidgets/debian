///////////////////////////////////////////////////////////////////////////////
// Name:        checklst.h
// Purpose:     wxCheckListBox class
// Author:      Robert Roebling
// Modified by:
// RCS-ID:      $Id: checklst.h,v 1.9 1999/10/11 10:05:33 RR Exp $
// Copyright:   (c) 1998 Robert Roebling
// Licence:     wxWindows licence
///////////////////////////////////////////////////////////////////////////////

#ifndef __GTKCHECKLISTH__
#define __GTKCHECKLISTH__

#ifdef __GNUG__
#pragma interface
#endif

#include "wx/defs.h"

#if wxUSE_CHECKLISTBOX

#include "wx/object.h"
#include "wx/list.h"
#include "wx/control.h"
#include "wx/listbox.h"

//-----------------------------------------------------------------------------
// classes
//-----------------------------------------------------------------------------

class wxCheckListBox;

//-----------------------------------------------------------------------------
// wxCheckListBox
//-----------------------------------------------------------------------------

class wxCheckListBox : public wxListBox
{
public:
    wxCheckListBox();
    wxCheckListBox(wxWindow *parent, wxWindowID id,
            const wxPoint& pos = wxDefaultPosition,
            const wxSize& size = wxDefaultSize,
            int nStrings = 0,
            const wxString *choices = (const wxString *)NULL,
            long style = 0,
            const wxValidator& validator = wxDefaultValidator,
            const wxString& name = wxListBoxNameStr);

    bool IsChecked( int index ) const;
    void Check( int index, bool check = TRUE );

    int GetItemHeight() const;
    
private:
    DECLARE_DYNAMIC_CLASS(wxCheckListBox)
};

#endif

#endif   //__GTKCHECKLISTH__
