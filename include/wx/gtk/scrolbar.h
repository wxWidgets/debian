/////////////////////////////////////////////////////////////////////////////
// Name:        scrolbar.h
// Purpose:
// Author:      Robert Roebling
// Id:          $Id: scrolbar.h,v 1.12 2000/01/20 14:16:13 RR Exp $
// Copyright:   (c) 1998 Robert Roebling
// Licence:   	wxWindows licence
/////////////////////////////////////////////////////////////////////////////


#ifndef __GTKSCROLLBARH__
#define __GTKSCROLLBARH__

#ifdef __GNUG__
#pragma interface
#endif

#include "wx/defs.h"

#if wxUSE_SCROLLBAR

#include "wx/object.h"
#include "wx/control.h"

//-----------------------------------------------------------------------------
// classes
//-----------------------------------------------------------------------------

class wxScrollBar;

//-----------------------------------------------------------------------------
// global data
//-----------------------------------------------------------------------------

extern const char *wxScrollBarNameStr;

//-----------------------------------------------------------------------------
// wxScrollBar
//-----------------------------------------------------------------------------

class wxScrollBar: public wxControl
{
public:
    wxScrollBar() 
       { m_adjust = (GtkAdjustment *) NULL; m_oldPos = 0.0; }
    inline wxScrollBar( wxWindow *parent, wxWindowID id,
           const wxPoint& pos = wxDefaultPosition,
           const wxSize& size = wxDefaultSize,
           long style = wxSB_HORIZONTAL,
           const wxValidator& validator = wxDefaultValidator,
           const wxString& name = wxScrollBarNameStr )
    {
        Create( parent, id, pos, size, style, validator, name );
    }
    bool Create( wxWindow *parent, wxWindowID id,
           const wxPoint& pos = wxDefaultPosition,
           const wxSize& size = wxDefaultSize,
           long style = wxSB_HORIZONTAL,
           const wxValidator& validator = wxDefaultValidator,
           const wxString& name = wxScrollBarNameStr );
    ~wxScrollBar();
    int GetThumbPosition() const;
    int GetThumbSize() const;
    int GetPageSize() const;
    int GetRange() const;
    virtual void SetThumbPosition( int viewStart );
    virtual void SetScrollbar( int position, int thumbSize, int range, int pageSize,
      bool refresh = TRUE );

    // Backward compatibility
    // ----------------------
    
    int GetValue(void) const;
    void SetValue( int viewStart );
    void GetValues( int *viewStart, int *viewLength, int *objectLength, int *pageLength) const;
    int GetViewLength() const;
    int GetObjectLength() const;
    void SetPageSize( int pageLength );
    void SetObjectLength( int objectLength );
    void SetViewLength( int viewLength );

    // implementation
    // --------------
    
    bool IsOwnGtkWindow( GdkWindow *window );
    void ApplyWidgetStyle();
  
    GtkAdjustment  *m_adjust;
    float           m_oldPos;
    
private:
    DECLARE_DYNAMIC_CLASS(wxScrollBar)
};

#endif

#endif
    // __GTKSCROLLBARH__
