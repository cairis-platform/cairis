#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ListCtrlComboPopup.py $ $Id: ListCtrlComboPopup.py 249 2010-05-30 17:07:31Z shaf $
import wx
import wx.combo

class ListCtrlComboPopup(wx.ListCtrl, wx.combo.ComboPopup):
  def __init__(self):
    self.PostCreate(wx.PreListCtrl())
    wx.combo.ComboPopup.__init__(self)

  def OnMotion(self, evt):
    item, flags = self.HitTest(evt.GetPosition())
    if (item >= 0):
      self.Select(item)
      self.curitem = item

  def OnLeftDown(self, evt):
    self.value = self.curitem
    self.Dismiss()

  def Create(self, parent):
    wx.ListCtrl.Create(self,parent,style = wx.LC_LIST | wx.LC_SINGLE_SEL | wx.SIMPLE_BORDER)
    self.Bind(wx.EVT_MOTION, self.OnMotion)
    self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
    return True

   
