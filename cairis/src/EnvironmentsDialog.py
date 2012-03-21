#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/EnvironmentsDialog.py $ $Id: EnvironmentsDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import ARM
from Environment import Environment
from EnvironmentDialog import EnvironmentDialog
from DialogClassParameters import DialogClassParameters
from EnvironmentParameters import EnvironmentParameters
from DimensionBaseDialog import DimensionBaseDialog

class EnvironmentsDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.ENVIRONMENTS_ID,'Environments',(930,300),'environment.png')
    self.rmFrame = parent
    idList = [armid.ENVIRONMENTS_LISTENVIRONMENTS_ID,armid.ENVIRONMENTS_BUTTONADD_ID,armid.ENVIRONMENTS_BUTTONDELETE_ID]
    columnList = ['Name','Description']
    self.buildControls(idList,columnList,self.dbProxy.getEnvironments,'environment')
    listCtrl = self.FindWindowById(armid.ENVIRONMENTS_LISTENVIRONMENTS_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,600)

  def addObjectRow(self,environmentListCtrl,listRow,environment):
    environmentListCtrl.InsertStringItem(listRow,environment.name())
    environmentListCtrl.SetStringItem(listRow,1,environment.description())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.ENVIRONMENT_ID,'Add environment',EnvironmentDialog,armid.ENVIRONMENT_BUTTONCOMMIT_ID,self.dbProxy.addEnvironment,True)
      self.addObject(addParameters)
      self.rmFrame.updateEnvironmentSelection(self.selectedLabel)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add environment',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(armid.ENVIRONMENT_ID,'Edit environment',EnvironmentDialog,armid.ENVIRONMENT_BUTTONCOMMIT_ID,self.dbProxy.updateEnvironment,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit environment',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No environment','Delete environment',self.dbProxy.deleteEnvironment)
      self.rmFrame.updateEnvironmentSelection()
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete environment',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
