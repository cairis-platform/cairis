#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DomainPropertiesDialog.py $ $Id: DomainPropertiesDialog.py 293 2010-07-11 17:32:06Z shaf $
import wx
import armid
import DomainProperty 
from DomainPropertyDialog import DomainPropertyDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class DomainPropertiesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.DOMAINPROPERTIES_ID,'Domain Properties',(930,300),'domainproperty.png')
    idList = [armid.DOMAINPROPERTIES_DOMAINPROPERTYLIST_ID,armid.DOMAINPROPERTIES_BUTTONADD_ID,armid.DOMAINPROPERTIES_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getDomainProperties,'domainproperty')
    listCtrl = self.FindWindowById(armid.DOMAINPROPERTIES_DOMAINPROPERTYLIST_ID)
    listCtrl.SetColumnWidth(0,300)
    listCtrl.SetColumnWidth(1,200)


  def addObjectRow(self,listCtrl,listRow,dp):
    listCtrl.InsertStringItem(listRow,dp.name())
    listCtrl.SetStringItem(listRow,1,dp.type())


  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.DOMAINPROPERTY_ID,'Add Domain Property',DomainPropertyDialog,armid.DOMAINPROPERTY_BUTTONCOMMIT_ID,self.dbProxy.addDomainProperty,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add Domain Property',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(armid.DOMAINPROPERTY_ID,'Edit Domain Property',DomainPropertyDialog,armid.DOMAINPROPERTY_BUTTONCOMMIT_ID,self.dbProxy.updateDomainProperty,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit Domain Property',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No Domain Property','Delete Domain Property',self.dbProxy.deleteDomainProperty)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete Domain Property',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
