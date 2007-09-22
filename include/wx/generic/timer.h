/////////////////////////////////////////////////////////////////////////////
// Name:        timer.h
// Purpose:     Generic implementation of wxTimer class
// Author:      Vaclav Slavik
// Id:          $Id: timer.h,v 1.2.2.1 2005/06/20 17:36:52 MR Exp $
// Copyright:   (c) 2001-2002 SciTech Software, Inc. (www.scitechsoft.com)
// Licence:     wxWindows licence
/////////////////////////////////////////////////////////////////////////////


#ifndef __WX_TIMER_H__
#define __WX_TIMER_H__

//-----------------------------------------------------------------------------
// wxTimer
//-----------------------------------------------------------------------------

class wxTimerDesc;

class WXDLLEXPORT wxTimer : public wxTimerBase
{
public:
    wxTimer() { Init(); }
    wxTimer(wxEvtHandler *owner, int id = -1) : wxTimerBase(owner, id)
        { Init(); }
    ~wxTimer();

    virtual bool Start(int millisecs = -1, bool oneShot = FALSE);
    virtual void Stop();

    virtual bool IsRunning() const;

    // implementation
    static void NotifyTimers();

protected:
    void Init();

private:
    wxTimerDesc *m_desc;
    
    DECLARE_ABSTRACT_CLASS(wxTimer)
};

#endif // __WX_TIMER_H__
