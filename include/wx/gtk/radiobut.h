/////////////////////////////////////////////////////////////////////////////
// Name:        wx/gtk/radiobut.h
// Purpose:
// Author:      Robert Roebling
// Id:          $Id: radiobut.h,v 1.19 2002/09/07 12:28:46 GD Exp $
// Copyright:   (c) 1998 Robert Roebling
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////


#ifndef __GTKRADIOBUTTONH__
#define __GTKRADIOBUTTONH__

#if defined(__GNUG__) && !defined(__APPLE__)
#pragma interface
#endif

//-----------------------------------------------------------------------------
// wxRadioButton
//-----------------------------------------------------------------------------

class wxRadioButton: public wxControl
{
public:
    wxRadioButton() { }
    wxRadioButton( wxWindow *parent,
                   wxWindowID id,
                   const wxString& label,
                   const wxPoint& pos = wxDefaultPosition,
                   const wxSize& size = wxDefaultSize,
                   long style = 0,
                   const wxValidator& validator = wxDefaultValidator,
                   const wxString& name = wxRadioButtonNameStr )
    {
        Create( parent, id, label, pos, size, style, validator, name );
    }

    bool Create( wxWindow *parent,
                 wxWindowID id,
                 const wxString& label,
                 const wxPoint& pos = wxDefaultPosition,
                 const wxSize& size = wxDefaultSize,
                 long style = 0,
                 const wxValidator& validator = wxDefaultValidator,
                 const wxString& name = wxRadioButtonNameStr );

    virtual void SetLabel(const wxString& label);
    virtual void SetValue(bool val);
    virtual bool GetValue() const;
    virtual bool Enable( bool enable = TRUE );

    // implementation

    virtual bool IsRadioButton() const { return TRUE; }

    GSList *m_radioButtonGroup;
    void ApplyWidgetStyle();
    bool IsOwnGtkWindow( GdkWindow *window );
    void OnInternalIdle();

    bool m_blockEvent;

protected:
    virtual wxSize DoGetBestSize() const;

private:
    DECLARE_DYNAMIC_CLASS(wxRadioButton)
};

#endif // __GTKRADIOBUTTONH__
