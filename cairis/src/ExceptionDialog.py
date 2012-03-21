#$URL$ $Id: ExceptionDialog.py 334 2010-11-07 19:44:00Z shaf $
import wx
import armid
import ARM
import WidgetFactory
from ExceptionPanel import ExceptionPanel
from Borg import Borg

class ExceptionDialog(wx.Dialog):
  def __init__(self,parent,envName,eName = '', eDimType = 'goal', eDimName = '', eCat = '', eDef = ''):
    wx.Dialog.__init__(self,parent,armid.EXCEPTION_ID,'Add Flow Exception',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,500))
    self.theEnvironmentName = envName
    self.theName = eName
    self.theDimensionType = eDimType
    self.theDimensionName = eDimName
    self.theCategory = eCat
    self.theDefinition = eDef
    self.panel = 0
    isCreate = True

    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ExceptionPanel(self,self.theEnvironmentName)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    if eName != '':
      self.SetLabel('Edit Flow Exception')
      self.commitVerb = 'Edit'
      self.panel.loadControls((eName,eDimType,eDimName,eCat,eDef))
      isCreate = False
    else:
      self.commitVerb = 'Add'
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.EXCEPTION_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.EXCEPTION_BUTTONCOMMIT_ID,self.onCommit)

    

  def onCommit(self,evt):
    commitLabel = self.commitVerb + ' Flow Exception'

    nameCtrl = self.FindWindowById(armid.EXCEPTION_TEXTNAME_ID)
    goalCtrl = self.FindWindowById(armid.EXCEPTION_COMBOGOALS_ID)
    typeCtrl = self.FindWindowById(armid.EXCEPTION_RADIOGOAL_ID)
    catCtrl = self.FindWindowById(armid.EXCEPTION_COMBOCATEGORY_ID)
    defCtrl = self.FindWindowById(armid.EXCEPTION_TEXTDEFINITION_ID)


    self.theName = nameCtrl.GetValue()
    if (typeCtrl.GetValue() == True):
      self.theDimensionType = 'goal'
    else:
      self.theDimensionType = 'requirement'
    self.theDimensionName = goalCtrl.GetValue()
    self.theCategory = catCtrl.GetValue()
    self.theDefinition = defCtrl.GetValue()


    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'Exception name cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDimensionName) == 0:
      dlg = wx.MessageDialog(self,self.theDimensionType + ' selection must be selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theCategory) == 0:
      dlg = wx.MessageDialog(self,'Category must be selected',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDefinition) == 0):
      dlg = wx.MessageDialog(self,'Definition cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    self.EndModal(armid.EXCEPTION_BUTTONCOMMIT_ID)

  def parameters(self):
    return (self.theName,self.theDimensionType,self.theDimensionName,self.theCategory,self.theDefinition)
