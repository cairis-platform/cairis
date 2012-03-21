#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ValueTypesDialog.py $ $Id: ValueTypesDialog.py 427 2011-02-27 12:29:59Z shaf $
import wx
import armid
from ValueTypeDialog import ValueTypeDialog
from ValueTypeDialogParameters import ValueTypeDialogParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class ValueTypesDialog(DimensionBaseDialog):
  def __init__(self,parent,value_type,defEnv = ''):
    label = '' 
    imageFile = ''
    self.theValueType = value_type
    self.theDefaultEnvironment = defEnv
    if (self.theValueType == 'asset_value'): 
      label = 'Asset values'
      imageFile = 'asset.png'
    elif (self.theValueType == 'threat_value'): 
      label = 'Threat values'
      imageFile = 'threat.png'
    elif (self.theValueType == 'countermeasure_value'): 
      label = 'Countermeasure values'
      imageFile = 'countermeasure.png'
    elif (self.theValueType == 'capability'): 
      label = 'Capability values'
      imageFile = 'attacker.png'
    elif (self.theValueType == 'motivation'): 
      label = 'Motivation values'
      imageFile = 'attacker.png'
    elif (self.theValueType == 'asset_type'): 
      label = 'Asset Type values'
      imageFile = 'asset.png'
    elif (self.theValueType == 'threat_type'): 
      label = 'Threat Type values'
      imageFile = 'threat.png'
    elif (self.theValueType == 'vulnerability_type'): 
      label = 'Vulnerability Type values'
      imageFile = 'asset.png'
    elif (self.theValueType == 'severity'): 
      label = 'Vulnerability Severity values'
      imageFile = 'vulnerability.png'
    elif (self.theValueType == 'likelihood'): 
      label = 'Threat Likelihood values'
      imageFile = 'threat.png'
    elif (self.theValueType == 'risk_class'): 
      label = 'Risk category values'
      imageFile = 'risk.png'
    else:
      exceptionText = 'Unknown value type ' + value_type
      raise ARM.ARMException(exceptionText)
    DimensionBaseDialog.__init__(self,parent,armid.VALUETYPES_ID,label,(930,300),imageFile)

    self.deleteFn = None
    if (self.theValueType == 'capability'): 
      self.deleteFn = self.dbProxy.deleteCapability
    elif (self.theValueType == 'motivation'): 
      self.deleteFn = self.dbProxy.deleteMotivation
    elif (self.theValueType == 'asset_type'): 
      self.deleteFn = self.dbProxy.deleteAssetType
    elif (self.theValueType == 'threat_type'): 
      self.deleteFn = self.dbProxy.deleteThreatType
    elif (self.theValueType == 'vulnerability_type'): 
      self.deleteFn = self.dbProxy.deleteVulnerabilityType

    idList = [armid.VALUETYPES_VALUELIST_ID,armid.VALUETYPES_BUTTONADD_ID,armid.VALUETYPES_BUTTONDELETE_ID]
    columnList = ['Name','Description']
    envName = ''
    self.buildControls(idList,columnList,self.dbProxy.getValueTypes,self.theValueType,self.theDefaultEnvironment)
    if (self.theValueType == 'asset_value'):
      comboCtrl = self.FindWindowById(armid.VALUETYPES_COMBOENVIRONMENT_ID)
      comboCtrl.SetValue(self.theDefaultEnvironment)
      wx.EVT_COMBOBOX(self,armid.VALUETYPES_COMBOENVIRONMENT_ID,self.onEnvironmentChange)

    self.listCtrl = self.FindWindowById(armid.VALUETYPES_VALUELIST_ID)
    self.listCtrl.SetColumnWidth(0,150)
    self.listCtrl.SetColumnWidth(1,700)


    if ((self.theValueType == 'asset_value') or (self.theValueType == 'threat_value') or (self.theValueType == 'risk_class') or (self.theValueType == 'countermeasure_value') or (self.theValueType == 'severity') or (self.theValueType == 'likelihood')):
      addButton = self.FindWindowById(armid.VALUETYPES_BUTTONADD_ID)
      addButton.Hide()
      deleteButton = self.FindWindowById(armid.VALUETYPES_BUTTONDELETE_ID)
      deleteButton.Hide()

  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.name())
    listCtrl.SetStringItem(listRow,1,objt.description())

  def onAdd(self,evt):
    try:
      addParameters = ValueTypeDialogParameters(armid.VALUETYPE_ID,'Add ' + self.theValueType,ValueTypeDialog,armid.VALUETYPE_BUTTONCOMMIT_ID,self.dbProxy.addValueType,True,self.theValueType)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add ' + self.theValueType,wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    assetId = selectedObjt.id()
    try:
      if (self.theValueType != 'asset_value'):
        updateParameters = ValueTypeDialogParameters(armid.VALUETYPE_ID,'Edit ' + self.theValueType,ValueTypeDialog,armid.VALUETYPE_BUTTONCOMMIT_ID,self.dbProxy.updateValueType,False,self.theValueType)
      else:
        envName = self.environmentCtrl.GetValue()
        updateParameters = ValueTypeDialogParameters(armid.VALUETYPE_ID,'Edit ' + self.theValueType,ValueTypeDialog,armid.VALUETYPE_BUTTONCOMMIT_ID,self.dbProxy.updateValueType,False,self.theValueType,envName)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit ' + self.theValueType,wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No ' + self.theValueType,'Delete ' + self.theValueType,self.deleteFn)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete ' + self.theValueType,wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onEnvironmentChange(self,evt):
    envName = self.environmentCtrl.GetStringSelection()
    self.listCtrl.DeleteAllItems()
    try:
      self.objts = self.dbProxy.getValueTypes(self.theValueType,envName)
      newObjts = {}
      listRow = 0
      for objt in self.objts:
        self.addObjectRow(self.listCtrl,listRow,objt)
        newObjts[objt.name()] = objt
        listRow += 1
      self.objts = newObjts
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Values',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
