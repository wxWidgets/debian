/////////////////////////////////////////////////////////////////////////////
// Name:        ddesetup.h
// Purpose:     DDE sample settings
// Author:      Julian Smart
// Modified by:
// Created:     25/01/99
// RCS-ID:      $Id: ddesetup.h,v 1.2 2000/03/10 05:32:40 GRG Exp $
// Copyright:   (c) Julian Smart
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

/*
 * Adjust this before compiling, to switch between real DDE and TCP/IP
 * implementations.
 */

// If 1, use real DDE. If 0, use TCP/IP

#ifdef __WXMSW__
#define wxUSE_DDE_FOR_SAMPLE 0
#else
#define wxUSE_DDE_FOR_SAMPLE 0
#endif

#if wxUSE_DDE_FOR_SAMPLE

#define wxConnection    wxDDEConnection
#define wxServer        wxDDEServer
#define wxClient        wxDDEClient

#include <wx/dde.h>

#else

#define wxConnection    wxTCPConnection
#define wxServer        wxTCPServer
#define wxClient        wxTCPClient

#include <wx/sckipc.h>

#endif

