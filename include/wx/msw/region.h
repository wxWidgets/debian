/////////////////////////////////////////////////////////////////////////////
// Name:        region.h
// Purpose:     wxRegion class
// Author:      Markus Holzem, Julian Smart
// Modified by:
// Created:     01/02/97
// RCS-ID:      $Id: region.h,v 1.8 2000/02/06 12:12:25 JS Exp $
// Copyright:   (c) Julian Smart
// Licence:   	wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_REGION_H_
#define _WX_REGION_H_

#ifdef __GNUG__
#pragma interface "region.h"
#endif

#include "wx/list.h"
#include "wx/gdiobj.h"
#include "wx/gdicmn.h"

class WXDLLEXPORT wxRect;
class WXDLLEXPORT wxPoint;

enum wxRegionContain {
	wxOutRegion = 0, wxPartRegion = 1, wxInRegion = 2
};

// So far, for internal use only
enum wxRegionOp {
wxRGN_AND,          // Creates the intersection of the two combined regions.
wxRGN_COPY,         // Creates a copy of the region identified by hrgnSrc1.
wxRGN_DIFF,         // Combines the parts of hrgnSrc1 that are not part of hrgnSrc2.
wxRGN_OR,           // Creates the union of two combined regions.
wxRGN_XOR           // Creates the union of two combined regions except for any overlapping areas.
};

class WXDLLEXPORT wxRegion : public wxGDIObject {
DECLARE_DYNAMIC_CLASS(wxRegion);
	friend class WXDLLEXPORT wxRegionIterator;
public:
    wxRegion(wxCoord x, wxCoord y, wxCoord w, wxCoord h);
    wxRegion(const wxPoint& topLeft, const wxPoint& bottomRight);
    wxRegion(const wxRect& rect);
    wxRegion(WXHRGN hRegion); // Hangs on to this region

	wxRegion(void);
	~wxRegion(void);

	//# Copying
	inline wxRegion(const wxRegion& r)
		{ Ref(r); }
	inline wxRegion& operator = (const wxRegion& r)
		{ Ref(r); return (*this); }

	//# Modify region
	// Clear current region
	void Clear(void);

	// Union rectangle or region with this.
	inline bool Union(wxCoord x, wxCoord y, wxCoord width, wxCoord height) { return Combine(x, y, width, height, wxRGN_OR); }
	inline bool Union(const wxRect& rect) { return Combine(rect, wxRGN_OR); }
	inline bool Union(const wxRegion& region) { return Combine(region, wxRGN_OR); }

	// Intersect rectangle or region with this.
	inline bool Intersect(wxCoord x, wxCoord y, wxCoord width, wxCoord height) { return Combine(x, y, width, height, wxRGN_AND); }
	inline bool Intersect(const wxRect& rect)  { return Combine(rect, wxRGN_AND); }
	inline bool Intersect(const wxRegion& region)  { return Combine(region, wxRGN_AND); }

	// Subtract rectangle or region from this:
    // Combines the parts of 'this' that are not part of the second region.
	inline bool Subtract(wxCoord x, wxCoord y, wxCoord width, wxCoord height) { return Combine(x, y, width, height, wxRGN_DIFF); }
	inline bool Subtract(const wxRect& rect)  { return Combine(rect, wxRGN_DIFF); }
	inline bool Subtract(const wxRegion& region)  { return Combine(region, wxRGN_DIFF); }

	// XOR: the union of two combined regions except for any overlapping areas.
	inline bool Xor(wxCoord x, wxCoord y, wxCoord width, wxCoord height) { return Combine(x, y, width, height, wxRGN_XOR); }
	inline bool Xor(const wxRect& rect)  { return Combine(rect, wxRGN_XOR); }
	inline bool Xor(const wxRegion& region)  { return Combine(region, wxRGN_XOR); }

	//# Information on region
	// Outer bounds of region
	void GetBox(wxCoord& x, wxCoord& y, wxCoord&w, wxCoord &h) const;
	wxRect GetBox(void) const ;

	// Is region empty?
	bool Empty(void) const;
    inline bool IsEmpty(void) const { return Empty(); }

	//# Tests
	// Does the region contain the point (x,y)?
	wxRegionContain Contains(wxCoord x, wxCoord y) const;
	// Does the region contain the point pt?
	wxRegionContain Contains(const wxPoint& pt) const;
	// Does the region contain the rectangle (x, y, w, h)?
	wxRegionContain Contains(wxCoord x, wxCoord y, wxCoord w, wxCoord h) const;
	// Does the region contain the rectangle rect?
	wxRegionContain Contains(const wxRect& rect) const;

// Internal
	bool Combine(wxCoord x, wxCoord y, wxCoord width, wxCoord height, wxRegionOp op);
	bool Combine(const wxRegion& region, wxRegionOp op);
	bool Combine(const wxRect& rect, wxRegionOp op);

    // Get internal region handle
    WXHRGN GetHRGN() const;
};

class WXDLLEXPORT wxRegionIterator : public wxObject {
DECLARE_DYNAMIC_CLASS(wxRegionIterator);
public:
	wxRegionIterator(void);
	wxRegionIterator(const wxRegion& region);
	~wxRegionIterator(void);

	void Reset(void) { m_current = 0; }
	void Reset(const wxRegion& region);

#ifndef __SALFORDC__
	operator bool (void) const { return (m_current < m_numRects); }
#endif

	bool HaveRects(void) const { return (m_current < m_numRects); }

	void operator ++ (void);
	void operator ++ (int);

	wxCoord GetX(void) const;
	wxCoord GetY(void) const;
	wxCoord GetW(void) const;
	wxCoord GetWidth(void) const { return GetW(); }
	wxCoord GetH(void) const;
	wxCoord GetHeight(void) const { return GetH(); }
    wxRect GetRect() const { return wxRect(GetX(), GetY(), GetWidth(), GetHeight()); }

private:
	long	 m_current;
	long	 m_numRects;
	wxRegion m_region;
    wxRect*  m_rects;
};

#endif
	// _WX_REGION_H_
