/////////////////////////////////////////////////////////////////////////////
// Name:        wx/palmos/sound.h
// Purpose:     wxSound class
// Author:      William Osborne - minimal working wxPalmOS port
// Modified by:
// Created:     10/13/04
// RCS-ID:      $Id: sound.h 69178 2011-09-21 15:08:02Z VZ $
// Copyright:   (c) William Osborne
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////

#ifndef _WX_SOUND_H_
#define _WX_SOUND_H_

#if wxUSE_SOUND

#include "wx/object.h"

class WXDLLIMPEXP_ADV wxSound : public wxSoundBase
{
public:
  wxSound();
  wxSound(const wxString& fileName, bool isResource = false);
  wxSound(size_t size, const void* data);
  virtual ~wxSound();

public:
  // Create from resource or file
  bool  Create(const wxString& fileName, bool isResource = false);
  // Create from data
  bool Create(size_t size, const void* data);

  bool  IsOk() const { return (m_waveData ? true : false); };

  static void Stop();

protected:
  bool  Free();

  bool DoPlay(unsigned flags) const;

private:
  wxByte* m_waveData;
  int   m_waveLength;
  bool  m_isResource;

    wxDECLARE_NO_COPY_CLASS(wxSound);
};
#endif
#endif

