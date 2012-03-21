#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PropertiesListCtrl.py $ $Id: PropertiesListCtrl.py 424 2011-02-25 21:29:47Z shaf $
import wx
import armid
import ARM
from PropertyDialog import PropertyDialog
from ValueDictionary import ValueDictionary

class PropertiesListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,values,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.theCurrentEnvironment = ''
    self.InsertColumn(0,'Property')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Value')
    self.SetColumnWidth(1,300)
    self.InsertColumn(2,'Rationale')
    self.SetColumnWidth(2,300)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.PROPERTIESLISTCTRL_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.PROPERTIESLISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedValue = ''
    self.theSelectedIdx = -1
    self.setProperties = {}
    self.valueLookup = values
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onItemActivated)
    wx.EVT_MENU(self.theDimMenu,armid.PROPERTIESLISTCTRL_MENUADD_ID,self.onAddProperty)
    wx.EVT_MENU(self.theDimMenu,armid.PROPERTIESLISTCTRL_MENUDELETE_ID,self.onDeleteProperty)

  def setEnvironment(self,environmentName):
    self.theCurrentEnvironment = environmentName
    if ((self.theCurrentEnvironment in self.setProperties) == False):
      self.setProperties[self.theCurrentEnvironment] = set([])

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onItemActivated(self,evt):
    x = evt.GetIndex()
    propertyName = self.GetItemText(x)
    valueItem = self.GetItem(x,1)
    rItem = self.GetItem(x,2)
    dlg = PropertyDialog(self,self.setProperties[self.theCurrentEnvironment],self.valueLookup.values())
    dlg.load(propertyName,valueItem.GetText(),rItem.GetText())
    if (dlg.ShowModal() == armid.PROPERTY_BUTTONADD_ID):
      pName = dlg.property()
      pValue = dlg.value()
      pRationale = dlg.rationale()
      idx = self.GetItemCount()
      self.SetStringItem(x,0,pName)
      self.SetStringItem(x,1,pValue)
      self.SetStringItem(x,2,pRationale)
      self.theSelectedValue = propertyName
      (self.setProperties[self.theCurrentEnvironment]).add(propertyName)

  def onAddProperty(self,evt):
    dlg = PropertyDialog(self,self.setProperties[self.theCurrentEnvironment],self.valueLookup.values())
    if (dlg.ShowModal() == armid.PROPERTY_BUTTONADD_ID):
      propertyName = dlg.property()
      propertyValue = dlg.value()
      propertyRationale = dlg.rationale()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,propertyName)
      self.SetStringItem(idx,1,propertyValue)
      self.SetStringItem(idx,2,propertyRationale)
      self.theSelectedValue = propertyName
      (self.setProperties[self.theCurrentEnvironment]).add(propertyName)

  def onDeleteProperty(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No property selected'
      errorLabel = 'Delete Security Property'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      selectedValue = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)
      (self.setProperties[self.theCurrentEnvironment]).remove(selectedValue)

  def load(self,syProperties,pRationale):
    cProperty = syProperties[armid.C_PROPERTY]
    cRationale = pRationale[armid.C_PROPERTY]
    if (cProperty != armid.NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Confidentiality')
      self.SetStringItem(idx,1,self.valueLookup.name(cProperty))
      self.SetStringItem(idx,2,cRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Confidentiality')

    iProperty = syProperties[armid.I_PROPERTY]
    iRationale = pRationale[armid.I_PROPERTY]
    if (iProperty != armid.NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Integrity')
      self.SetStringItem(idx,1,self.valueLookup.name(iProperty))
      self.SetStringItem(idx,2,iRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Integrity')

    avProperty = syProperties[armid.AV_PROPERTY]
    avRationale = pRationale[armid.AV_PROPERTY]
    if (avProperty != armid.NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Availability')
      self.SetStringItem(idx,1,self.valueLookup.name(avProperty))
      self.SetStringItem(idx,2,avRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Availability')

    acProperty = syProperties[armid.AC_PROPERTY]
    acRationale = pRationale[armid.AC_PROPERTY]
    if (acProperty != armid.NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Accountability')
      self.SetStringItem(idx,1,self.valueLookup.name(acProperty))
      self.SetStringItem(idx,2,acRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Accountability')

    anProperty = syProperties[armid.AN_PROPERTY]
    anRationale = pRationale[armid.AN_PROPERTY]
    if (anProperty != armid.NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Anonymity')
      self.SetStringItem(idx,1,self.valueLookup.name(anProperty))
      self.SetStringItem(idx,2,anRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Anonymity')

    panProperty = syProperties[armid.PAN_PROPERTY]
    panRationale = pRationale[armid.PAN_PROPERTY]
    if (panProperty != armid.NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Pseudonymity')
      self.SetStringItem(idx,1,self.valueLookup.name(panProperty))
      self.SetStringItem(idx,2,panRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Pseudonymity')

    unlProperty = syProperties[armid.UNL_PROPERTY]
    unlRationale = pRationale[armid.UNL_PROPERTY]
    if (unlProperty != armid.NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Unlinkability')
      self.SetStringItem(idx,1,self.valueLookup.name(unlProperty))
      self.SetStringItem(idx,2,unlRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Unlinkability')

    unoProperty = syProperties[armid.UNO_PROPERTY]
    unoRationale = pRationale[armid.UNO_PROPERTY]
    if (unoProperty != armid.NONE_VALUE):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Unobservability')
      self.SetStringItem(idx,1,self.valueLookup.name(unoProperty))
      self.SetStringItem(idx,2,unoRationale)
      (self.setProperties[self.theCurrentEnvironment]).add('Unobservability')

  def properties(self):
    workingProperties = [0,0,0,0,0,0,0,0]
    workingRationale = ['None','None','None','None','None','None','None','None']
    for x in range(self.GetItemCount()):
      propertyName = self.GetItemText(x)
      valueItem = self.GetItem(x,1)
      rItem = self.GetItem(x,2)
      propertyValue = valueItem.GetText()
      propertyRationale = rItem.GetText()
      if (propertyName == 'Confidentiality'):
        workingProperties[armid.C_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[armid.C_PROPERTY] = propertyRationale
      elif (propertyName == 'Integrity'):
        workingProperties[armid.I_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[armid.I_PROPERTY] = propertyRationale
      elif (propertyName == 'Availability'):
        workingProperties[armid.AV_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[armid.AV_PROPERTY] = propertyRationale
      elif (propertyName == 'Accountability'):
        workingProperties[armid.AC_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[armid.AC_PROPERTY] = propertyRationale
      elif (propertyName == 'Anonymity'):
        workingProperties[armid.AN_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[armid.AN_PROPERTY] = propertyRationale
      elif (propertyName == 'Pseudonymity'):
        workingProperties[armid.PAN_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[armid.PAN_PROPERTY] = propertyRationale
      elif (propertyName == 'Unlinkability'):
        workingProperties[armid.UNL_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[armid.UNL_PROPERTY] = propertyRationale
      elif (propertyName == 'Unobservability'):
        workingProperties[armid.UNO_PROPERTY] = self.valueLookup.id(propertyValue)
        workingRationale[armid.UNO_PROPERTY] = propertyRationale
    return (workingProperties,workingRationale)
