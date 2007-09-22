/////////////////////////////////////////////////////////////////////////////
// Name:        sckstrm.h
// Purpose:     wxSocket*Stream
// Author:      Guilhem Lavaux
// Modified by:
// Created:     17/07/97
// RCS-ID:      $Id: sckstrm.cpp,v 1.9 1999/09/15 00:17:15 GRG Exp $
// Copyright:   (c)
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////
#ifdef __GNUG__
#pragma implementation "sckstrm.h"
#endif

// For compilers that support precompilation, includes "wx.h".
#include "wx/wxprec.h"

#ifdef __BORLANDC__
  #pragma hdrstop
#endif

#ifndef WX_PRECOMP
  #include "wx/defs.h"
#endif

#if wxUSE_SOCKETS && wxUSE_STREAMS

#include "wx/stream.h"
#include "wx/socket.h"
#include "wx/sckstrm.h"

// ---------------------------------------------------------------------------
// wxSocketOutputStream
// ---------------------------------------------------------------------------

wxSocketOutputStream::wxSocketOutputStream(wxSocketBase& s)
  : m_o_socket(&s)
{
}

wxSocketOutputStream::~wxSocketOutputStream()
{
}

size_t wxSocketOutputStream::OnSysWrite(const void *buffer, size_t size)
{
  size_t ret;

  ret = m_o_socket->Write((const char *)buffer, size).LastCount();

  if (m_o_socket->Error())
    m_lasterror = wxStream_WRITE_ERR;
  else
    m_lasterror = wxStream_NOERROR;

  return ret;

}

// ---------------------------------------------------------------------------
// wxSocketInputStream
// ---------------------------------------------------------------------------

wxSocketInputStream::wxSocketInputStream(wxSocketBase& s)
 : m_i_socket(&s)
{
}

wxSocketInputStream::~wxSocketInputStream()
{
}

size_t wxSocketInputStream::OnSysRead(void *buffer, size_t size)
{
  size_t ret;

  ret = m_i_socket->Read((char *)buffer, size).LastCount();

  if (m_i_socket->Error())
    m_lasterror = wxStream_READ_ERR;
  else
    m_lasterror = wxStream_NOERROR;

  return ret;
}

// ---------------------------------------------------------------------------
// wxSocketStream
// ---------------------------------------------------------------------------

wxSocketStream::wxSocketStream(wxSocketBase& s)
  : wxSocketInputStream(s), wxSocketOutputStream(s)
{
}

wxSocketStream::~wxSocketStream()
{
}

#endif
  // wxUSE_STREAMS && wxUSE_SOCKETS
