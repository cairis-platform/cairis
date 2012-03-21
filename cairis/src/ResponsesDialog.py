#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ResponsesDialog.py $ $Id: ResponsesDialog.py 293 2010-07-11 17:32:06Z shaf $
import wx
import armid
import Risk
from ResponseDialog import ResponseDialog
from DialogClassParameters import DialogClassParameters
from ResponseDialogParameters import ResponseDialogParameters
from AcceptEnvironmentPanel import AcceptEnvironmentPanel
from TransferEnvironmentPanel import TransferEnvironmentPanel
from MitigateEnvironmentPanel import MitigateEnvironmentPanel
from DimensionBaseDialog import DimensionBaseDialog
import ARM

class ResponsesDialog(DimensionBaseDialog):
  def __init__(self,parent):
    DimensionBaseDialog.__init__(self,parent,armid.RESPONSES_ID,'Responses',(800,300),'response.png')
    self.theMainWindow = parent
    idList = [armid.RESPONSES_LISTRESPONSES_ID,armid.RESPONSES_BUTTONADD_ID,armid.RESPONSES_BUTTONDELETE_ID]
    columnList = ['Name','Type']
    self.buildControls(idList,columnList,self.dbProxy.getResponses,'response')
    listCtrl = self.FindWindowById(armid.RESPONSES_LISTRESPONSES_ID)
    listCtrl.SetColumnWidth(0,300)


  def addObjectRow(self,mitListCtrl,listRow,response):
    mitListCtrl.InsertStringItem(listRow,response.name())
    mitListCtrl.SetStringItem(listRow,1,response.__class__.__name__)

  def onAdd(self,evt):
    try:
      riskDict = self.dbProxy.getDimensionNames('risk')
      if (len(riskDict) == 0):
        dlg = wx.MessageDialog(self,'Cannot mitigate for non-existing risks','Add response',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
        return
      responseTypes = ['Accept','Transfer','Mitigate']
      from DimensionNameDialog import DimensionNameDialog
      rtDlg = DimensionNameDialog(self,'response',responseTypes,'Select',(300,200))
      if (rtDlg.ShowModal() == armid.DIMNAME_BUTTONACTION_ID):
        responseType = rtDlg.dimensionName()
        responsePanel = MitigateEnvironmentPanel
        if (responseType == 'Accept'):
          responsePanel = AcceptEnvironmentPanel
        elif (responseType == 'Transfer'):
          responsePanel = TransferEnvironmentPanel
        addParameters = ResponseDialogParameters(armid.RESPONSE_ID,'Add response',ResponseDialog,armid.RESPONSE_BUTTONCOMMIT_ID,self.dbProxy.addResponse,True,responsePanel,responseType)
        self.addObject(addParameters)
      rtDlg.Destroy()
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add response',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return

  def onUpdate(self,evt):
    try:
      selectedObjt = self.objts[self.selectedLabel]
      responseType = selectedObjt.responseType()
      responsePanel = MitigateEnvironmentPanel
      if (responseType == 'Accept'):
        responsePanel = AcceptEnvironmentPanel
      elif (responseType == 'Transfer'):
        responsePanel = TransferEnvironmentPanel
      updateParameters = ResponseDialogParameters(armid.RESPONSE_ID,'Edit response',ResponseDialog,armid.RESPONSE_BUTTONCOMMIT_ID,self.dbProxy.updateResponse,False,responsePanel,responseType)
      self.updateObject(selectedObjt,updateParameters)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Edit response',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy

  def onDelete(self,evt):
    try:
      self.dbProxy.associateGrid(self.theMainWindow.FindWindowById(armid.ID_REQGRID))
      self.deleteObject('No response','Delete response',self.dbProxy.deleteResponse)
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Delete response',wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
