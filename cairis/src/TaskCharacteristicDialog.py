#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaCharacteristicDialog.py $ $Id: PersonaCharacteristicDialog.py 285 2010-07-01 21:32:07Z shaf $
import wx
import armid
from PersonaCharacteristicNotebook import PersonaCharacteristicNotebook
from TaskCharacteristicParameters import TaskCharacteristicParameters
import WidgetFactory

class TaskCharacteristicDialog(wx.Dialog):
  def __init__(self,parent,parameters):
    wx.Dialog.__init__(self,parent,parameters.id(),parameters.label(),style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(700,300))
    self.theTaskName = ''
    self.theModalQualifier = ''
    self.theCharacteristic = ''
    self.theGrounds = []
    self.theWarrant = []
    self.theBacking = []
    self.theRebuttal = []
    self.isCreate = True
    self.showTaskCombo = True

    self.theId = -1
    self.panel = 0
    self.inTask = False
    if (parameters.__class__.__name__ == 'TaskCharacteristicDialogParameters'):
      self.inTask = True
      self.showTaskCombo = parameters.showTask()

    if (self.inTask):
      self.theTaskName = parameters.task()

    self.commitVerb = 'Add'
    
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = PersonaCharacteristicNotebook(self,True,self.showTaskCombo)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.TASKCHARACTERISTIC_BUTTONCOMMIT_ID,True),0,wx.CENTER)

    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.TASKCHARACTERISTIC_BUTTONCOMMIT_ID,self.onCommit)

  def load(self,objt):
    self.theId = objt.id()
    buttonCtrl = self.FindWindowById(armid.TASKCHARACTERISTIC_BUTTONCOMMIT_ID)
    buttonCtrl.SetLabel('Edit')
    self.panel.loadControls(objt)

    if (self.inTask and self.showTaskCombo):
      pCtrl = self.FindWindowById(armid.TASKCHARACTERISTIC_COMBOTASK_ID)
      pCtrl.SetValue(objt.task())

    self.commitVerb = 'Edit'

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' task characteristic'

    qualCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_TEXTQUALIFIER_ID)
    charCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_TEXTCHARACTERISTIC_ID)
    groundsCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_LISTGROUNDS_ID)
    warrantCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_LISTWARRANT_ID)
    rebuttalCtrl = self.FindWindowById(armid.PERSONACHARACTERISTIC_LISTREBUTTAL_ID)

    self.theModalQualifier = qualCtrl.GetValue()
    self.theCharacteristic = charCtrl.GetValue()
    self.theGrounds = groundsCtrl.dimensions()
    self.theWarrant = warrantCtrl.dimensions()
    self.theRebuttal = rebuttalCtrl.dimensions()
 
    
    if (self.inTask == False):
      pCtrl = self.FindWindowById(armid.TASKCHARACTERISTIC_COMBOTASK_ID)
      self.theTaskName = pCtrl.GetValue()

    if len(self.theTaskName) == 0:
      dlg = wx.MessageDialog(self,'Task cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theModalQualifier) == 0:
      dlg = wx.MessageDialog(self,'Model Qualifier cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theCharacteristic) == 0:
      dlg = wx.MessageDialog(self,'Characteristic cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theGrounds) == 0:
      dlg = wx.MessageDialog(self,'Some grounds for this characteristic must be provided',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.TASKCHARACTERISTIC_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = TaskCharacteristicParameters(self.theTaskName,self.theModalQualifier,self.theCharacteristic,self.theGrounds,self.theWarrant,[],self.theRebuttal)
    parameters.setId(self.theId)
    return parameters
