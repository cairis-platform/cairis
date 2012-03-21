#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SingleEnvironmentPropertiesListCtrl.py $ $Id: SingleEnvironmentPropertiesListCtrl.py 424 2011-02-25 21:29:47Z shaf $
import wx
import armid
import ARM
from PropertyDialog import PropertyDialog
from ValueDictionary import ValueDictionary

class SingleEnvironmentPropertiesListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,values,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.theCurrentEnvironment = ''
    self.InsertColumn(0,'Property')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Value')
    self.SetColumnWidth(1,300)
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.PROPERTIESLISTCTRL_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.PROPERTIESLISTCTRL_MENUDELETE_ID,'Delete')
    self.theSelectedValue = ''
    self.theSelectedIdx = -1
    self.valueLookup = values
    self.setProperties = set([])
    self.theConfidentialityValue = 'None'
    self.theIntegrityValue = 'None'
    self.theAvailabilityValue = 'None'
    self.theAccountabilityValue = 'None'
    self.theAnonymityValue = 'None'
    self.thePseudonymityValue = 'None'
    self.theUnlinkabilityValue = 'None'
    self.theUnobservabilityValue = 'None'
    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    wx.EVT_MENU(self.theDimMenu,armid.PROPERTIESLISTCTRL_MENUADD_ID,self.onAddProperty)
    wx.EVT_MENU(self.theDimMenu,armid.PROPERTIESLISTCTRL_MENUDELETE_ID,self.onDeleteProperty)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def OnRightDown(self,evt):
    self.PopupMenu(self.theDimMenu)

  def onAddProperty(self,evt):
    dlg = PropertyDialog(self,self.setProperties,self.valueLookup.values())
    if (dlg.ShowModal() == armid.PROPERTY_BUTTONADD_ID):
      propertyName = dlg.property()
      propertyValue = dlg.value()
      idx = self.GetItemCount()
      self.InsertStringItem(idx,propertyName)
      self.SetStringItem(idx,1,propertyValue)
      self.theSelectedValue = propertyName
      self.setProperties.add(propertyName)

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
      self.setProperties.remove(selectedValue)

  def load(self,cProperty,iProperty,avProperty,acProperty,anProperty,panProperty,unlProperty,unoProperty):
    if (cProperty != 'None'):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Confidentiality')
      self.SetStringItem(idx,1,cProperty)
      self.setProperties.add('Confidentiality')

    if (iProperty != 'None'):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Integrity')
      self.SetStringItem(idx,1,iProperty)
      self.setProperties.add('Integrity')

    if (avProperty != 'None'):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Availability')
      self.SetStringItem(idx,1,avProperty)
      self.setProperties.add('Availability')

    if (acProperty != 'None'):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Accountability')
      self.SetStringItem(idx,1,acProperty)
      self.setProperties.add('Accountability')

    if (anProperty != 'None'):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Anonymity')
      self.SetStringItem(idx,1,anProperty)
      self.setProperties.add('Anonymity')

    if (panProperty != 'None'):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Pseudonymity')
      self.SetStringItem(idx,1,panProperty)
      self.setProperties.add('Pseudonymity')

    if (unlProperty != 'None'):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Unlinkability')
      self.SetStringItem(idx,1,unlProperty)
      self.setProperties.add('Unlinkability')

    if (unoProperty != 'None'):
      idx = self.GetItemCount()
      self.InsertStringItem(idx,'Unobservability')
      self.SetStringItem(idx,1,unoProperty)
      self.setProperties.add('Unobservability')

  def properties(self):
    for x in range(self.GetItemCount()):
      propertyName = self.GetItemText(x)
      valueItem = self.GetItem(x,1)
      propertyValue = valueItem.GetText()
      if (propertyName == 'Confidentiality'):
        self.theConfidentialityValue = propertyValue 
      elif (propertyName == 'Integrity'):
        self.theIntegrityValue = propertyValue 
      elif (propertyName == 'Availability'):
        self.theAvailabilityValue = propertyValue 
      elif (propertyName == 'Accountability'):
        self.theAccountabilityValue = propertyValue 
      elif (propertyName == 'Anonymity'):
        self.theAnonymityValue = propertyValue 
      elif (propertyName == 'Pseudonymity'):
        self.thePseudonymityValue = propertyValue 
      elif (propertyName == 'Unlinkability'):
        self.theUnlinkabilityValue = propertyValue 
      elif (propertyName == 'Unobservability'):
        self.theUnobservabilityValue = propertyValue 
    return [self.theConfidentialityValue,self.theIntegrityValue,self.theAvailabilityValue,self.theAccountabilityValue,self.theAnonymityValue,self.thePseudonymityValue,self.theUnlinkabilityValue,self.theUnobservabilityValue]
