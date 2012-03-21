#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/IRISApp.py $ $Id: IRISApp.py 249 2010-05-30 17:07:31Z shaf $

import wx
import BorgFactory
from ARM import *
from RMFrame import RMFrame

RMFRAME_ID = 50

class IRISApp(wx.App):
  def OnInit(self):
    try:
      BorgFactory.initialise()
      self.frame = RMFrame(None,RMFRAME_ID,'CAIRIS')
      self.frame.Show()
      self.SetTopWindow(self.frame)
      return True
    except ARMException, e:
      print 'Error starting iris: ',e
      return False
