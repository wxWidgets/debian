
import wx

#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        dpc = wx.DatePickerCtrl(self, size=(120,-1),
                                style = wx.DP_DROPDOWN
                                      | wx.DP_SHOWCENTURY
                                      | wx.DP_ALLOWNONE )
        self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged, dpc)
        sizer.Add(dpc, 0, wx.ALL, 50)

        if 'wxMSW' in wx.PlatformInfo:
            # In this case the widget used above will be a native date
            # picker, so show the generic one too.            
            dpc = wx.GenericDatePickerCtrl(self, size=(120,-1),
                                           style = wx.TAB_TRAVERSAL
                                               | wx.DP_DROPDOWN
                                               | wx.DP_SHOWCENTURY
                                               | wx.DP_ALLOWNONE )
            self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged, dpc)
            sizer.Add(dpc, 0, wx.LEFT, 50)


    def OnDateChanged(self, evt):
        self.log.write("OnDateChanged: %s\n" % evt.GetDate())

#----------------------------------------------------------------------

def runTest(frame, nb, log):
    win = TestPanel(nb, log)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>wx.DatePickerCtrl</center></h2>

This control allows the user to select a date. Unlike
wx.calendar.CalendarCtrl, which is a relatively big control,
wx.DatePickerCtrl is implemented as a small window showing the
currently selected date. The control can be edited using the keyboard,
and can also display a popup window for more user-friendly date
selection, depending on the styles used and the platform.

</body></html>
"""



if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

