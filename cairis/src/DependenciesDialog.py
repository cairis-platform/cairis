#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DependenciesDialog.py $ $Id: DependenciesDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import Dependency
from DependencyDialog import DependencyDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class DependenciesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.DEPENDENCIES_ID,'Dependencies',(1080,300),'dependencyassociation.png')
    idList = [armid.DEPENDENCIES_DEPENDENCYLIST_ID,armid.DEPENDENCIES_BUTTONADD_ID,armid.DEPENDENCIES_BUTTONDELETE_ID]
    columnList = ['Environment','Depender','Dependee','Noun','Dependency']
    self.buildControls(idList,columnList,self.dbProxy.getDependencies,'dependency')
    listCtrl = self.FindWindowById(armid.DEPENDENCIES_DEPENDENCYLIST_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,150)
    listCtrl.SetColumnWidth(2,150)
    listCtrl.SetColumnWidth(3,150)
    listCtrl.SetColumnWidth(4,150)


  def addObjectRow(self,listCtrl,listRow,dependency):
    listCtrl.InsertStringItem(listRow,dependency.environment())
    listCtrl.SetStringItem(listRow,1,dependency.depender())
    listCtrl.SetStringItem(listRow,2,dependency.dependee())
    listCtrl.SetStringItem(listRow,3,dependency.dependencyType())
    listCtrl.SetStringItem(listRow,4,dependency.dependency())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.DEPENDENCY_ID,'Add depencency',DependencyDialog,armid.DEPENDENCY_BUTTONCOMMIT_ID,self.dbProxy.addDependency,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add dependency',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def dependencyLabel(self):
    listCtrl = self.FindWindowById(armid.DEPENDENCIES_DEPENDENCYLIST_ID)
    env = listCtrl.GetItemText(self.selectedIdx)
    depender = listCtrl.GetItem(self.selectedIdx,1)
    dependee = listCtrl.GetItem(self.selectedIdx,2)
    dependencyType = listCtrl.GetItem(self.selectedIdx,3)
    dependency = listCtrl.GetItem(self.selectedIdx,4)
    return env + '/' + depender.GetText() + '/' + dependee.GetText() + '/' + dependency.GetText()

  def deprecatedLabel(self):
    listCtrl = self.FindWindowById(armid.DEPENDENCIES_DEPENDENCYLIST_ID)
    env = listCtrl.GetItemText(self.selectedIdx)
    depender = listCtrl.GetItem(self.selectedIdx,1)
    dependee = listCtrl.GetItem(self.selectedIdx,2)
    dependency = listCtrl.GetItem(self.selectedIdx,4)
    return env + '/' + depender.GetText() + '/' + dependee.GetText() + '/' + dependency.GetText()
  
  def onUpdate(self,evt):
    selectedObjt = self.objts[self.dependencyLabel()]
    goalId = selectedObjt.id()
    try:
      updateParameters = DialogClassParameters(armid.DEPENDENCY_ID,'Edit depencency',DependencyDialog,armid.DEPENDENCY_BUTTONCOMMIT_ID,self.dbProxy.updateDependency,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit dependency',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No dependency','Delete dependency',self.dbProxy.deleteDependency)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete dependency',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
