/////////////////////////////////////////////////////////////////////////////
// Name:        imagjpeg.h
// Purpose:     wxImage JPEG handler
// Author:      Vaclav Slavik
// RCS-ID:      $Id: imagjpeg.h,v 1.3 2002/08/31 11:29:10 GD Exp $
// Copyright:   (c) Vaclav Slavik
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_IMAGJPEG_H_
#define _WX_IMAGJPEG_H_

#if defined(__GNUG__) && !defined(__APPLE__)
#pragma interface "imagjpeg.h"
#endif

#include "wx/image.h"

//-----------------------------------------------------------------------------
// wxJPEGHandler
//-----------------------------------------------------------------------------

#if wxUSE_LIBJPEG
class WXDLLEXPORT wxJPEGHandler: public wxImageHandler
{
  DECLARE_DYNAMIC_CLASS(wxJPEGHandler)

public:

  inline wxJPEGHandler()
  {
      m_name = "JPEG file";
      m_extension = "jpg";
      m_type = wxBITMAP_TYPE_JPEG;
      m_mime = "image/jpeg";
  };

#if wxUSE_STREAMS
  virtual bool LoadFile( wxImage *image, wxInputStream& stream, bool verbose=TRUE, int index=-1 );
  virtual bool SaveFile( wxImage *image, wxOutputStream& stream, bool verbose=TRUE );
  virtual bool DoCanRead( wxInputStream& stream );
#endif
};
#endif



#endif
  // _WX_IMAGJPEG_H_

