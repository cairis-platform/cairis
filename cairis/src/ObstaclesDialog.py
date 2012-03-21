#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ObstaclesDialog.py $ $Id: ObstaclesDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import Obstacle
from ObstacleDialog import ObstacleDialog
from DialogClassParameters import DialogClassParameters
import ARM
from DimensionBaseDialog import DimensionBaseDialog

class ObstaclesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.OBSTACLES_ID,'Obstacles',(930,300),'obstacle.png')
    idList = [armid.OBSTACLES_OBSTACLELIST_ID,armid.OBSTACLES_BUTTONADD_ID,armid.OBSTACLES_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getObstacles,'obstacle')
    listCtrl = self.FindWindowById(armid.OBSTACLES_OBSTACLELIST_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,listCtrl,listRow,obstacle):
    listCtrl.InsertStringItem(listRow,obstacle.name())


  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.OBSTACLE_ID,'Add obstacle',ObstacleDialog,armid.OBSTACLE_BUTTONCOMMIT_ID,self.dbProxy.addObstacle,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add obstacle',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
    try:
      updateParameters = DialogClassParameters(armid.OBSTACLE_ID,'Edit obstacle',ObstacleDialog,armid.OBSTACLE_BUTTONCOMMIT_ID,self.dbProxy.updateObstacle,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit obstacle',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.deleteObject('No obstacle','Delete obstacle',self.dbProxy.deleteObstacle)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete obstacle',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy
