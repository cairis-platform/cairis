#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/BehaviouralCharacteristicsDialog.py $ $Id: BehaviouralCharacteristicsDialog.py 465 2011-05-01 16:00:00Z shaf $
import wx
import armid
import PersonaCharacteristic
from PersonaCharacteristicDialog import PersonaCharacteristicDialog
from PersonaCharacteristicDialogParameters import PersonaCharacteristicDialogParameters
from TaskCharacteristicDialog import TaskCharacteristicDialog
from TaskCharacteristicDialogParameters import TaskCharacteristicDialogParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog
from Borg import Borg

class BehaviouralCharacteristicsDialog(DimensionBaseDialog):
  def __init__(self,parent,aName,bvName = ''):
    b = Borg()
    self.dbProxy = b.dbProxy
    windowLabel = 'Persona Characteristics'
    windowIcon = 'persona.png'
    getFn = self.dbProxy.getPersonaBehaviouralCharacteristics
    if (bvName == ''):
      windowLabel = 'Task Characteristics'
      windowIcon = 'task.png'
      getFn = self.dbProxy.getTaskSpecificCharacteristics
    DimensionBaseDialog.__init__(self,parent,armid.PERSONACHARACTERISTICS_ID,windowLabel,(930,300),windowIcon)
    self.theMainWindow = parent
    self.theName = aName
    self.theBehaviouralVariable = bvName
    idList = [armid.PERSONACHARACTERISTICS_CHARLIST_ID,armid.PERSONACHARACTERISTICS_BUTTONADD_ID,armid.PERSONACHARACTERISTICS_BUTTONDELETE_ID]
    columnList = ['Characteristic']
    self.buildControls(idList,columnList,getFn,'behavioural_characteristic')
    listCtrl = self.FindWindowById(armid.PERSONACHARACTERISTICS_CHARLIST_ID)
    listCtrl.SetColumnWidth(0,700)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.characteristic())

  def onAdd(self,evt):
    try:
      if (self.theBehaviouralVariable != ''):
        addParameters = PersonaCharacteristicDialogParameters(armid.PERSONACHARACTERISTIC_ID,'Add Persona Characteristic',PersonaCharacteristicDialog,armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.addPersonaCharacteristic,True,self.theName,self.theBehaviouralVariable)
      else:
        addParameters = TaskCharacteristicDialogParameters(armid.TASKCHARACTERISTIC_ID,'Add Task Characteristic',TaskCharacteristicDialog,armid.TASKCHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.addTaskCharacteristic,True,self.theName,False)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.deprecatedLabel()]
    objtId = selectedObjt.id()
    try:
      if (self.theBehaviouralVariable != ''):
        updateParameters = PersonaCharacteristicDialogParameters(armid.PERSONACHARACTERISTIC_ID,'Edit Persona Characteristic',PersonaCharacteristicDialog,armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.updatePersonaCharacteristic,False,self.theName,self.theBehaviouralVariable)
      else:
        updateParameters = TaskCharacteristicDialogParameters(armid.TASKCHARACTERISTIC_ID,'Edit Task Characteristic',TaskCharacteristicDialog,armid.TASKCHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.updateTaskCharacteristic,False,self.theName,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      if (self.theBehaviouralVariable != ''):
        self.deleteObject('No persona characteristic','Delete persona characteristic',self.dbProxy.deletePersonaCharacteristic)
      else:
        self.deleteObject('No task characteristic','Delete task characteristic',self.dbProxy.deleteTaskCharacteristic)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete task characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy


  def deprecatedLabel(self):
    listCtrl = self.FindWindowById(armid.PERSONACHARACTERISTICS_CHARLIST_ID)
    charItem = listCtrl.GetItem(listCtrl.theSelectedIdx,0)
    charTxt = charItem.GetText()
    if (self.theBehaviouralVariable != ''):
      pcLabel = self.theName + '/' + self.theBehaviouralVariable + '/' + charTxt
    else:
      pcLabel = self.theName + '/' + charTxt
    return pcLabel
