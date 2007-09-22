/////////////////////////////////////////////////////////////////////////////
// Name:        wx/config.h
// Purpose:     wxConfig base header
// Author:      Julian Smart
// Modified by:
// Created:
// Copyright:   (c) Julian Smart
// RCS-ID:      $Id: config.h,v 1.17.6.1 2005/05/04 18:23:24 JS Exp $
// Licence:     wxWindows Licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_CONFIG_H_BASE_
#define _WX_CONFIG_H_BASE_

#include "wx/confbase.h"

#if defined(__WXMSW__) && wxUSE_CONFIG_NATIVE
#  ifdef __WIN32__
#    include "wx/msw/regconf.h"
#else
#    include "wx/msw/iniconf.h"
#  endif
#else
#    include "wx/fileconf.h"
#endif

#endif
    // _WX_CONFIG_H_BASE_
