///////////////////////////////////////////////////////////////////////////////
// Name:        gtk/dataobj.h
// Purpose:     declaration of the wxDataObject
// Author:      Robert Roebling
// RCS-ID:      $Id: dataobj.h,v 1.17 1999/10/21 10:23:28 RR Exp $
// Copyright:   (c) 1998, 1999 Vadim Zeitlin, Robert Roebling
// Licence:     wxWindows license
///////////////////////////////////////////////////////////////////////////////

#ifndef _WX_GTK_DATAOBJ_H_
#define _WX_GTK_DATAOBJ_H_

#ifdef __GNUG__
    #pragma interface "dataobj.h"
#endif

// ----------------------------------------------------------------------------
// wxDataObject is the same as wxDataObjectBase under wxGTK
// ----------------------------------------------------------------------------

class wxDataObject : public wxDataObjectBase
{
public:
    wxDataObject();

    virtual bool IsSupportedFormat( const wxDataFormat& format, Direction dir = Get ) const;
};

#endif // _WX_GTK_DATAOBJ_H_

