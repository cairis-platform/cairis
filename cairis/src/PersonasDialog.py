#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonasDialog.py $ $Id: PersonasDialog.py 523 2011-11-04 18:07:01Z shaf $
import wx
import armid
from PersonaDialog import PersonaDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class PersonasDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.PERSONAS_ID,'Personas',(800,300),'persona.png')
    idList = [armid.PERSONAS_PERSONALIST_ID,armid.PERSONAS_BUTTONADD_ID,armid.PERSONAS_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getPersonas,'persona')
    listCtrl = self.FindWindowById(armid.PERSONAS_PERSONALIST_ID)
    listCtrl.SetColumnWidth(0,100)
    listCtrl.SetColumnWidth(1,600)


  def addObjectRow(self,personaListCtrl,listRow,persona):
    personaListCtrl.InsertStringItem(listRow,persona.name())
    personaListCtrl.SetStringItem(listRow,1,persona.type())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.PERSONA_ID,'Add persona',PersonaDialog,armid.PERSONA_BUTTONCOMMIT_ID,self.dbProxy.addPersona,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add persona',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(armid.PERSONA_ID,'Edit persona',PersonaDialog,armid.PERSONA_BUTTONCOMMIT_ID,self.dbProxy.updatePersona,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit persona',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onDelete(self,evt):
    try:
      self.deleteObject('No persona','Delete persona',self.dbProxy.deletePersona)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete persona',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
