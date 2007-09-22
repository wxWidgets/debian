/////////////////////////////////////////////////////////////////////////////
// Name:        control.h
// Purpose:
// Author:      Robert Roebling
// Id:          $Id: control.h,v 1.16.2.2 2005/06/20 17:36:58 MR Exp $
// Copyright:   (c) 1998 Robert Roebling, Julian Smart
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef __GTKCONTROLH__
#define __GTKCONTROLH__

#include "wx/defs.h"
#include "wx/object.h"
#include "wx/list.h"
#include "wx/window.h"

//-----------------------------------------------------------------------------
// classes
//-----------------------------------------------------------------------------

class wxControl;

//-----------------------------------------------------------------------------
// wxControl
//-----------------------------------------------------------------------------

class wxControl : public wxControlBase
{
public:
    wxControl();
    wxControl(wxWindow *parent, wxWindowID id,
             const wxPoint& pos = wxDefaultPosition,
             const wxSize& size = wxDefaultSize, long style = 0,
             const wxValidator& validator = wxDefaultValidator,
             const wxString& name = wxControlNameStr)
    {
        Create(parent, id, pos, size, style, validator, name);
    }

    bool Create(wxWindow *parent, wxWindowID id,
            const wxPoint& pos = wxDefaultPosition,
            const wxSize& size = wxDefaultSize, long style = 0,
            const wxValidator& validator = wxDefaultValidator,
            const wxString& name = wxControlNameStr);

    // this function will filter out '&' characters and will put the accelerator
    // char (the one immediately after '&') into m_chAccel (TODO not yet)
    virtual void SetLabel( const wxString &label );
    virtual wxString GetLabel() const;

protected:
    virtual wxSize DoGetBestSize() const;
#ifdef __WXGTK20__
    wxString PrepareLabelMnemonics( const wxString &label ) const;
#endif

    wxString   m_label;
    char       m_chAccel;  // enabled to avoid breaking binary compatibility later on

private:
    DECLARE_DYNAMIC_CLASS(wxControl)
};

#endif // __GTKCONTROLH__
