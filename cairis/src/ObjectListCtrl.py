#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ObjectListCtrl.py $ $Id: ObjectListCtrl.py 249 2010-05-30 17:07:31Z shaf $
import wx

class ObjectListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
