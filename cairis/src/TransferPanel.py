#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TransferPanel.py $ $Id: TransferPanel.py 429 2011-02-27 17:34:37Z shaf $

import wx
import armid
import WidgetFactory
from Borg import Borg
from numpy import *
from ResponseParameters import ResponseParameters

class TransferPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.RESPONSE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theDescription = ''
    self.theCommitVerb = 'Create'
    self.theRisks = []

  def buildControls(self,isCreate,isUpdateable = True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildDimensionListSizer(self,'Risks',(100,82),armid.RESPONSE_LISTRISKS_ID,'risk',self.dbProxy),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,60),armid.RESPONSE_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    self.SetSizer(mainSizer)

  def loadControls(self,response,isReadOnly = False):
    risksCtrl = self.FindWindowById(armid.RESPONSE_LISTRISKS_ID)
    descriptionCtrl = self.FindWindowById(armid.RESPONSE_TEXTDESCRIPTION_ID)
    
    risksCtrl.Set(response.risks())
    descriptionCtrl.SetValue(response.description())
    if (isReadOnly):
      rationaleCtrl.Disable()
      risksCtrl.Disable()
    self.theCommitVerb = 'Edit'

  def commit(self):
    risksCtrl = self.FindWindowById(armid.RESPONSE_LISTRISKS_ID)
    descriptionCtrl = self.FindWindowById(armid.RESPONSE_TEXTDESCRIPTION_ID)

    commitLabel = self.theCommitVerb + ' transfer'

    self.theDescription = descriptionCtrl.GetValue()

    if (risksCtrl.GetCount() == 0):
      dlg = wx.MessageDialog(self,'At least one risk needs to be accepted',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theDescription) == 0):
      dlg = wx.MessageDialog(self,'No transfer description',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    else:
      for x in range(risksCtrl.GetCount()):
        riskName = risksCtrl.GetString(x)
        self.theRisks.append(riskName)
      return 0


  def parameters(self,responseName,responseCost,responseRoles):
   responseType = 'Transfer'
   responseProperties =  array((0,0,0,3,0,0,0,0))
   detectionPoint = 'none'
   detectionMechanism = -1
   targets = []
   return ResponseParameters(responseName,responseType,self.theDescription,responseCost,responseProperties,detectionPoint,detectionMechanism,self.theRisks,targets,responseRoles)
