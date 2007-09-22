/////////////////////////////////////////////////////////////////////////////
// Name:        dcmemory.cpp
// Purpose:     wxMemoryDC class
// Author:      Julian Smart
// Modified by:
// Created:     01/02/97
// RCS-ID:      $Id: dcmemory.cpp,v 1.25.2.1 2005/06/20 17:43:54 MR Exp $
// Copyright:   (c) Julian Smart and Markus Holzem
// Licence:     wxWindows licence
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

#ifndef WX_PRECOMP
    #include "wx/utils.h"
    #include "wx/log.h"
#endif

#include "wx/msw/private.h"

#include "wx/dcmemory.h"

// ----------------------------------------------------------------------------
// wxWin macros
// ----------------------------------------------------------------------------

IMPLEMENT_DYNAMIC_CLASS(wxMemoryDC, wxDC)

// ============================================================================
// implementation
// ============================================================================

// ----------------------------------------------------------------------------
// wxMemoryDC
// ----------------------------------------------------------------------------

wxMemoryDC::wxMemoryDC()
{
    CreateCompatible(NULL);

    Init();
}

wxMemoryDC::wxMemoryDC(wxDC *dc)
{
    wxCHECK_RET( dc, _T("NULL dc in wxMemoryDC ctor") );

    dc->BeginDrawing();

    CreateCompatible(dc);

    dc->EndDrawing();

    Init();
}

void wxMemoryDC::Init()
{
    if ( m_ok )
    {
        SetBrush(*wxWHITE_BRUSH);
        SetPen(*wxBLACK_PEN);

        // the background mode is only used for text background and is set in
        // DrawText() to OPAQUE as required, otherwise always TRANSPARENT
        ::SetBkMode( GetHdc(), TRANSPARENT );
    }
}

bool wxMemoryDC::CreateCompatible(wxDC *dc)
{
    m_hDC = (WXHDC)::CreateCompatibleDC(dc ? GetHdcOf(*dc) : NULL);

    // as we created the DC, we must delete it in the dtor
    m_bOwnsDC = TRUE;

    m_ok = m_hDC != 0;

    return m_ok;
}

void wxMemoryDC::SelectObject(const wxBitmap& bitmap)
{
    // select old bitmap out of the device context
    if ( m_oldBitmap )
    {
        ::SelectObject(GetHdc(), (HBITMAP) m_oldBitmap);
        if ( m_selectedBitmap.Ok() )
        {
            m_selectedBitmap.SetSelectedInto(NULL);
            m_selectedBitmap = wxNullBitmap;
        }
    }

    // check for whether the bitmap is already selected into a device context
    wxCHECK_RET( !bitmap.GetSelectedInto() ||
                 (bitmap.GetSelectedInto() == this),
                 wxT("Bitmap is selected in another wxMemoryDC, delete the first wxMemoryDC or use SelectObject(NULL)") );

    m_selectedBitmap = bitmap;
    WXHBITMAP hBmp = m_selectedBitmap.GetHBITMAP();
    if ( !hBmp )
        return;

    m_selectedBitmap.SetSelectedInto(this);
    hBmp = (WXHBITMAP)::SelectObject(GetHdc(), (HBITMAP)hBmp);

    if ( !hBmp )
    {
        wxLogLastError(wxT("SelectObject(memDC, bitmap)"));

        wxFAIL_MSG(wxT("Couldn't select a bitmap into wxMemoryDC"));
    }
    else if ( !m_oldBitmap )
    {
        m_oldBitmap = hBmp;
    }
}

void wxMemoryDC::DoGetSize(int *width, int *height) const
{
    if ( m_selectedBitmap.Ok() )
    {
        *width = m_selectedBitmap.GetWidth();
        *height = m_selectedBitmap.GetHeight();
    }
    else
    {
        *width = 0;
        *height = 0;
    }
}

// the rest of this file deals with drawing rectangles workaround, disabled by
// default

#define wxUSE_MEMORY_DC_DRAW_RECTANGLE 0

#if wxUSE_MEMORY_DC_DRAW_RECTANGLE

// For some reason, drawing a rectangle on a memory DC has problems.
// Use this substitute if we can.
static void wxDrawRectangle(wxDC& dc, wxCoord x, wxCoord y, wxCoord width, wxCoord height)
{
    wxBrush brush(dc.GetBrush());
    wxPen pen(dc.GetPen());
    if (brush.Ok() && brush.GetStyle() != wxTRANSPARENT)
    {
        HBRUSH hBrush = (HBRUSH) brush.GetResourceHandle() ;
        if (hBrush)
        {
            RECT rect;
            rect.left = x; rect.top = y;
            rect.right = x + width - 1;
            rect.bottom = y + height - 1;
            ::FillRect((HDC) dc.GetHDC(), &rect, hBrush);
        }
    }
    width --; height --;
    if (pen.Ok() && pen.GetStyle() != wxTRANSPARENT)
    {
        dc.DrawLine(x, y, x + width, y);
        dc.DrawLine(x, y, x, y + height);
        dc.DrawLine(x, y+height, x+width, y + height);
        dc.DrawLine(x+width, y+height, x+width, y);
    }
}

#endif // wxUSE_MEMORY_DC_DRAW_RECTANGLE

void wxMemoryDC::DoDrawRectangle(wxCoord x, wxCoord y, wxCoord width, wxCoord height)
{
    // Set this to 1 to work around an apparent video driver bug
    // (visible with e.g. 70x70 rectangle on a memory DC; see Drawing sample)
#if wxUSE_MEMORY_DC_DRAW_RECTANGLE
    if (m_brush.Ok() && m_pen.Ok() &&
        (m_brush.GetStyle() == wxSOLID || m_brush.GetStyle() == wxTRANSPARENT) &&
        (m_pen.GetStyle() == wxSOLID || m_pen.GetStyle() == wxTRANSPARENT) &&
        (GetLogicalFunction() == wxCOPY))
    {
        wxDrawRectangle(* this, x, y, width, height);
    }
    else
#endif // wxUSE_MEMORY_DC_DRAW_RECTANGLE
    {
        wxDC::DoDrawRectangle(x, y, width, height);
    }
}

