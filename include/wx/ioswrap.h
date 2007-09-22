///////////////////////////////////////////////////////////////////////////////
// Name:        ioswrap.h
// Purpose:     includes the correct iostream headers for current compiler
// Author:      Vadim Zeitlin
// Modified by:
// Created:     03.02.99
// RCS-ID:      $Id: ioswrap.h,v 1.3 1999/06/27 22:06:33 VZ Exp $
// Copyright:   (c) 1998 Vadim Zeitlin <zeitlin@dptmaths.ens-cachan.fr>
// Licence:     wxWindows license
///////////////////////////////////////////////////////////////////////////////

#if wxUSE_STD_IOSTREAM

#if wxUSE_IOSTREAMH
    // N.B. BC++ doesn't have istream.h, ostream.h
#   include <iostream.h>
#else
#   include <iostream>
#   if defined(__VISUALC__) || defined(__MWERKS__)
        using namespace std;
#   endif
#endif

#endif
  // wxUSE_STD_IOSTREAM

