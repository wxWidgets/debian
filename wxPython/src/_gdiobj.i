/////////////////////////////////////////////////////////////////////////////
// Name:        _gdiobj.i
// Purpose:     SWIG interface for wxGDIObject
//
// Author:      Robin Dunn
//
// Created:     13-Sept-2003
// RCS-ID:      $Id: _gdiobj.i 50779 2007-12-17 23:45:06Z RD $
// Copyright:   (c) 2003 by Total Control Software
// Licence:     wxWindows license
/////////////////////////////////////////////////////////////////////////////

// Not a %module

//---------------------------------------------------------------------------
%newgroup

MustHaveApp(wxGDIObject);

class wxGDIObject : public wxObject {
public:
    //wxGDIObject();      ****  It's an ABC
    ~wxGDIObject();

    bool IsNull() const;
    bool IsOk() const;
    %pythoncode { Ok = IsOk }    
};

//---------------------------------------------------------------------------
