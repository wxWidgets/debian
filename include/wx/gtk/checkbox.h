/////////////////////////////////////////////////////////////////////////////
// Name:        wx/gtk/checkbox.h
// Purpose:
// Author:      Robert Roebling
// Id:          $Id: checkbox.h,v 1.24.2.1 2005/06/20 17:36:57 MR Exp $
// Copyright:   (c) 1998 Robert Roebling
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef __GTKCHECKBOXH__
#define __GTKCHECKBOXH__

// ----------------------------------------------------------------------------
// wxCheckBox
// ----------------------------------------------------------------------------

class wxCheckBox : public wxCheckBoxBase
{
public:
    wxCheckBox();
    wxCheckBox( wxWindow *parent, wxWindowID id, const wxString& label,
            const wxPoint& pos = wxDefaultPosition,
            const wxSize& size = wxDefaultSize, long style = 0,
            const wxValidator& validator = wxDefaultValidator,
            const wxString& name = wxCheckBoxNameStr)
    {
        Create(parent, id, label, pos, size, style, validator, name);
    }
    bool Create(wxWindow *parent,
                wxWindowID id,
                const wxString& label,
                const wxPoint& pos = wxDefaultPosition,
                const wxSize& size = wxDefaultSize,
                long style = 0,
                const wxValidator& validator = wxDefaultValidator,
                const wxString& name = wxCheckBoxNameStr );

    void SetValue( bool state );
    bool GetValue() const;

    virtual void SetLabel( const wxString& label );
    virtual bool Enable( bool enable = TRUE );

    // implementation
    // --------------

    void ApplyWidgetStyle();
    bool IsOwnGtkWindow( GdkWindow *window );
    void OnInternalIdle();

    GtkWidget *m_widgetCheckbox;
    GtkWidget *m_widgetLabel;

    bool       m_blockEvent;

protected:
    virtual wxSize DoGetBestSize() const;

private:
    DECLARE_DYNAMIC_CLASS(wxCheckBox)
};

#endif // __GTKCHECKBOXH__
