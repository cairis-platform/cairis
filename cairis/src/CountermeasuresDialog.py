#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/CountermeasuresDialog.py $ $Id: CountermeasuresDialog.py 293 2010-07-11 17:32:06Z shaf $
import wx
import armid
import Risk
from CountermeasureDialog import CountermeasureDialog
from DialogClassParameters import DialogClassParameters
from DimensionBaseDialog import DimensionBaseDialog
import ARM

class CountermeasuresDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.COUNTERMEASURES_ID,'Countermeasures',(800,300),'countermeasure.png')
    self.theMainWindow = parent
    idList = [armid.COUNTERMEASURES_LISTCOUNTERMEASURES_ID,armid.COUNTERMEASURES_BUTTONADD_ID,armid.COUNTERMEASURES_BUTTONDELETE_ID]
    columnList = ['Name']
    self.buildControls(idList,columnList,self.dbProxy.getCountermeasures,'countermeasure')
    listCtrl = self.FindWindowById(armid.COUNTERMEASURES_LISTCOUNTERMEASURES_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,listCtrl,listRow,countermeasure):
    listCtrl.InsertStringItem(listRow,countermeasure.name())

  def onAdd(self,evt):
    try:
      addParameters = DialogClassParameters(armid.COUNTERMEASURE_ID,'Add countermeasure',CountermeasureDialog,armid.COUNTERMEASURE_BUTTONCOMMIT_ID,self.dbProxy.addCountermeasure,True)
      self.addObject(addParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add countermeasure',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    try:
      selectedObjt = self.objts[self.selectedLabel]
      updateParameters = DialogClassParameters(armid.COUNTERMEASURE_ID,'Edit countermeasure',CountermeasureDialog,armid.COUNTERMEASURE_BUTTONCOMMIT_ID,self.dbProxy.updateCountermeasure,False)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit countermeasure',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.dbProxy.associateGrid(self.theMainWindow.FindWindowById(armid.ID_REQGRID))
      self.deleteObject('No countermeasure','Delete countermeasure',self.dbProxy.deleteCountermeasure)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete countermeasure',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
