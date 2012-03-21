#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaCharacteristicsDialog.py $ $Id: PersonaCharacteristicsDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import PersonaCharacteristic
from PersonaCharacteristicDialog import PersonaCharacteristicDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class PersonaCharacteristicsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.PERSONACHARACTERISTICS_ID,'Persona Characteristics',(930,300),'persona.png')
    self.theMainWindow = parent
    idList = [armid.PERSONACHARACTERISTICS_CHARLIST_ID,armid.PERSONACHARACTERISTICS_BUTTONADD_ID,armid.PERSONACHARACTERISTICS_BUTTONDELETE_ID]
    columnList = ['Persona','Variable','Characteristic']
    self.buildControls(idList,columnList,self.dbProxy.getPersonaCharacteristics,'persona_characteristic')
    listCtrl = self.FindWindowById(armid.PERSONACHARACTERISTICS_CHARLIST_ID)
    listCtrl.SetColumnWidth(0,100)
    listCtrl.SetColumnWidth(1,100)
    listCtrl.SetColumnWidth(2,700)


  def addObjectRow(self,listCtrl,listRow,objt):
    listCtrl.InsertStringItem(listRow,objt.persona())
    listCtrl.SetStringItem(listRow,1,objt.behaviouralVariable())
    listCtrl.SetStringItem(listRow,2,objt.characteristic())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.PERSONACHARACTERISTIC_ID,'Add Persona Characteristic',PersonaCharacteristicDialog,armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.addPersonaCharacteristic,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add persona characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.deprecatedLabel()]
    objtId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.PERSONACHARACTERISTIC_ID,'Edit Persona Characteristic',PersonaCharacteristicDialog,armid.PERSONACHARACTERISTIC_BUTTONCOMMIT_ID,self.dbProxy.updatePersonaCharacteristic,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit persona characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No persona characteristic','Delete persona characteristic',self.dbProxy.deletePersonaCharacteristic)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete persona characteristic',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def deprecatedLabel(self):
    listCtrl = self.FindWindowById(armid.PERSONACHARACTERISTICS_CHARLIST_ID)
    pItem = listCtrl.GetItem(self.selectedIdx,0)
    pTxt = pItem.GetText()
    bvItem = listCtrl.GetItem(self.selectedIdx,1)
    bvTxt = bvItem.GetText()
    charItem = listCtrl.GetItem(self.selectedIdx,2)
    charTxt = charItem.GetText()
    pcLabel = pTxt + '/' + bvTxt + '/' + charTxt
    return pcLabel
