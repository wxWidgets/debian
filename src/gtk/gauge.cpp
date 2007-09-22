/////////////////////////////////////////////////////////////////////////////
// Name:        gauge.cpp
// Purpose:
// Author:      Robert Roebling
// Id:          $Id: gauge.cpp,v 1.17 1999/11/27 16:45:59 RR Exp $
// Copyright:   (c) 1998 Robert Roebling
// Licence:   	wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifdef __GNUG__
#pragma implementation "gauge.h"
#endif

#include "wx/gauge.h"

#if wxUSE_GAUGE

#include <gdk/gdk.h>
#include <gtk/gtk.h>

//-----------------------------------------------------------------------------
// wxGauge
//-----------------------------------------------------------------------------

IMPLEMENT_DYNAMIC_CLASS(wxGauge,wxControl)

bool wxGauge::Create( wxWindow *parent, wxWindowID id,  int range,
    const wxPoint& pos, const wxSize& size,
    long style, const wxValidator& validator, const wxString& name )
{
    m_needParent = TRUE;
  
    if (!PreCreation( parent, pos, size ) ||
        !CreateBase( parent, id, pos, size, style, validator, name ))
    {
        wxFAIL_MSG( wxT("wxGauge creation failed") );
	return FALSE;
    }

    m_rangeMax = range;
    m_gaugePos = 0;
    m_useProgressBar = TRUE;
  
    m_widget = gtk_progress_bar_new();
  
    m_parent->DoAddChild( this );
  
    PostCreation();
  
    Show( TRUE );
    
    return TRUE;
}

void wxGauge::SetRange( int r )
{
    m_rangeMax = r;
    if (m_gaugePos > m_rangeMax) m_gaugePos = m_rangeMax;
  
    gtk_progress_bar_update( GTK_PROGRESS_BAR(m_widget), ((float)m_gaugePos)/m_rangeMax );
}

void wxGauge::SetValue( int pos )
{
    m_gaugePos = pos;
    if (m_gaugePos > m_rangeMax) m_gaugePos = m_rangeMax;
  
    gtk_progress_bar_update( GTK_PROGRESS_BAR(m_widget), ((float)m_gaugePos)/m_rangeMax );
}

int wxGauge::GetRange() const
{
    return m_rangeMax;
}

int wxGauge::GetValue() const
{
    return m_gaugePos;
}

void wxGauge::ApplyWidgetStyle()
{
    SetWidgetStyle();
    gtk_widget_set_style( m_widget, m_widgetStyle );
}

#endif
