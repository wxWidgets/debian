/////////////////////////////////////////////////////////////////////////////
// Name:        wx_cw_d.h
// Purpose:     wxWindows definitions for CodeWarrior builds (Debug)
// Author:      Stefan Csomor
// Modified by:
// Created:     12/10/98
// RCS-ID:      $Id: wx_cw_d.h,v 1.5 1999/11/05 09:15:41 SC Exp $
// Copyright:   (c) Stefan Csomor
// Licence:   	wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_CW__
#define _WX_CW__

#if __option(profile)
#error "profiling is not supported in debug versions"
#else
#ifdef __cplusplus
	#if __POWERPC__
		#include <wx_PPC++_d.mch>
	#elif __INTEL__
		#include <wx_x86++_d.mch>
	#elif __CFM68K__
		#include <wx_cfm++_d.mch>
	#else
		#include <wx_68k++_d.mch>
	#endif
#else
	#if __POWERPC__
		#include <wx_PPC_d.mch>
	#elif __INTEL__
		#include <wx_x86_d.mch>
	#elif __CFM68K__
		#include <wx_cfm_d.mch>
	#else
		#include <wx_68k_d.mch>
	#endif
#endif
#endif

#endif
    // _WX_CW__
