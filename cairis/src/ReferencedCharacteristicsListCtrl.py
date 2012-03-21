#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ReferencedCharacteristicsListCtrl.py $ $Id: ReferencedCharacteristicsListCtrl.py 260 2010-06-17 14:19:36Z shaf $
import wx
import armid
from Borg import Borg

from ARM import *

class ReferencedCharacteristicsListCtrl(wx.ListCtrl):

  def __init__(self,parent,winId,dimName):
    wx.ListCtrl.__init__(self,parent,winId,style=wx.LC_REPORT)
    self.theParentDialog = parent
    self.theTraceMenu = wx.Menu()
    self.theDimensionName = dimName
    self.theTraceMenu.Append(armid.DRLC_MENU_REFERENCEDCHARACTERISTICS_ID,'Referenced Characteristics')
    wx.EVT_MENU(self,armid.DRLC_MENU_REFERENCEDCHARACTERISTICS_ID,self.onReferencedCharacteristics)
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.onRightClick)


  def onRightClick(self,evt):
    self.PopupMenu(self.theTraceMenu)

  def onReferencedCharacteristics(self,evt):
    docRef = self.theParentDialog.objts[self.theParentDialog.selectedLabel]
    refName = docRef.name()
    try:
      b = Borg()
      dbProxy = b.dbProxy
      refChars = dbProxy.referenceUse(refName,self.theDimensionName)
      print refChars
    except ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Referenced characteristics',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
