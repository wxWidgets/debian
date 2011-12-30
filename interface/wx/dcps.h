/////////////////////////////////////////////////////////////////////////////
// Name:        dcps.h
// Purpose:     interface of wxPostScriptDC
// Author:      wxWidgets team
// RCS-ID:      $Id: dcps.h 69300 2011-10-04 07:45:08Z RD $
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

/**
    @class wxPostScriptDC

    This defines the wxWidgets Encapsulated PostScript device context, which
    can write PostScript files on any platform. See wxDC for descriptions of
    the member functions.

    @library{wxbase}
    @category{dc}
*/
class wxPostScriptDC : public wxDC
{
public:
    wxPostScriptDC();

    /**
        Constructs a PostScript printer device context from a wxPrintData object.
    */
    wxPostScriptDC(const wxPrintData& printData);

};

