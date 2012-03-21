#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RolesDialog.py $ $Id: RolesDialog.py 412 2011-01-17 09:15:43Z shaf $
import wx
import armid
from Role import Role
from RoleDialog import RoleDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class RolesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.ROLES_ID,'Roles',(800,300),'role.png')
    idList = [armid.ROLES_LISTROLES_ID,armid.ROLES_BUTTONADD_ID,armid.ROLES_BUTTONDELETE_ID]
    columnList = ['Name','Short Code','Type']
    self.buildControls(idList,columnList,self.dbProxy.getRoles,'role')
    listCtrl = self.FindWindowById(armid.ROLES_LISTROLES_ID)
    listCtrl.SetColumnWidth(0,150)
    listCtrl.SetColumnWidth(1,100)
    listCtrl.SetColumnWidth(2,400)


  def addObjectRow(self,listCtrl,listRow,role):
    listCtrl.InsertStringItem(listRow,role.name())
    listCtrl.SetStringItem(listRow,1,role.shortCode())
    listCtrl.SetStringItem(listRow,2,role.type())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.ROLE_ID,'Add role',RoleDialog,armid.ROLE_BUTTONCOMMIT_ID,self.dbProxy.addRole,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add role',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(armid.ROLE_ID,'Edit role',RoleDialog,armid.ROLE_BUTTONCOMMIT_ID,self.dbProxy.updateRole,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit role',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onDelete(self,evt):
    try:
      self.deleteObject('No role','Delete role',self.dbProxy.deleteRole)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete role',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return
