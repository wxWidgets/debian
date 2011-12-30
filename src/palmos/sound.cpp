/////////////////////////////////////////////////////////////////////////////
// Name:        src/palmos/sound.cpp
// Purpose:     wxSound
// Author:      William Osborne - minimal working wxPalmOS port
// Modified by:
// Created:     10/13/04
// RCS-ID:      $Id: sound.cpp 69178 2011-09-21 15:08:02Z VZ $
// Copyright:   (c) William Osborne
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

// For compilers that support precompilation, includes "wx.h".
#include "wx/wxprec.h"

#if defined(__BORLANDC__)
#pragma hdrstop
#endif

#if wxUSE_SOUND

#ifndef WX_PRECOMP
#include "wx/wx.h"
#endif

#include "wx/file.h"
#include "wx/sound.h"
#include "wx/palmos/private.h"

wxSound::wxSound()
  : m_waveData(NULL), m_waveLength(0), m_isResource(false)
{
}

wxSound::wxSound(const wxString& sFileName, bool isResource)
  : m_waveData(NULL), m_waveLength(0), m_isResource(isResource)
{
}

wxSound::wxSound(size_t size, const void* data)
  : m_waveData(NULL), m_waveLength(0), m_isResource(false)
{
}

wxSound::~wxSound()
{
}

bool wxSound::Create(const wxString& fileName, bool isResource)
{
    return false;
}

bool wxSound::Create(size_t size, const void* data)
{
    return false;
}

bool wxSound::DoPlay(unsigned flags) const
{
    return false;
}

bool wxSound::Free()
{
    return false;
}

/*static*/ void wxSound::Stop()
{
}

#endif // wxUSE_SOUND
