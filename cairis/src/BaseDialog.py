import wx
import armid
from ResponseListCtrl import ResponseListCtrl
from CountermeasureListCtrl import CountermeasureListCtrl
from SecurityPatternListCtrl import SecurityPatternListCtrl
from TemplateAssetListCtrl import TemplateAssetListCtrl
from TraceableList import TraceableList
from ReferencedCharacteristicsListCtrl import ReferencedCharacteristicsListCtrl
from UseCaseListCtrl import UseCaseListCtrl
from ObjectListCtrl import ObjectListCtrl


class BaseDialog(wx.Dialog):
  def __init__(self,parent,winId,winLabel,initSize):
    wx.Dialog.__init__(self,parent,winId,winLabel,style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=initSize)

  
  def buildTraceListCtrl(parent,winId,columnNames,traces):
    listCtrl = wx.ListCtrl(parent,winId,style=wx.LC_REPORT)
    for idx,columnName in enumerate(columnNames):
      listCtrl.InsertColumn(idx,columnName)

    b = Borg()
    dbProxy = b.dbProxy
    listRow  = 0
    for idx, objt in enumerate(traces):
      listCtrl.InsertStringItem(objt.fromObject())
      listCtrl.SetColumnWidth(0,75)
      listCtrl.SetStringItem(listRow,1,objt.fromName())
      listCtrl.SetColumnWidth(1,250)
      listCtrl.SetStringItem(objt.toObject())
      listCtrl.SetColumnWidth(2,75)
      listCtrl.SetStringItem(listRow,3,objt.toName())
      listCtrl.SetColumnWidth(3,125)
      listRow += 1
    return listCtrl

  def buildListCtrl(parent,winId,columnNames,objtFn,dimName,envName = ''):
    listCtrl = 0
    if (dimName == 'response'):
      listCtrl = ResponseListCtrl(parent,winId)
    elif (dimName == 'countermeasure'):
      listCtrl = CountermeasureListCtrl(parent,winId)
    elif (dimName == 'securitypattern'):
      listCtrl = SecurityPatternListCtrl(parent,winId)
    elif (dimName == 'template_asset'):
      listCtrl = TemplateAssetListCtrl(parent,winId)
    elif (dimName == 'scenario'):
      listCtrl = TraceableList(parent,winId,'scenario')
    elif (dimName == 'asset'):
      listCtrl = TraceableList(parent,winId,'asset')
    elif (dimName == 'goal'):
      listCtrl = TraceableList(parent,winId,'goal')
    elif (dimName == 'obstacle'):
      listCtrl = TraceableList(parent,winId,'obstacle')
    elif (dimName == 'task'):
      listCtrl = TraceableList(parent,winId,'task')
    elif (dimName == 'document_reference'):
      listCtrl = ReferencedCharacteristicsListCtrl(parent,winId,'document_reference')
    elif (dimName == 'concept_reference'):
      listCtrl = ReferencedCharacteristicsListCtrl(parent,winId,'concept_reference')
    elif (dimName == 'usecase'):
      listCtrl = UseCaseListCtrl(parent,winId)
    else:
      listCtrl = ObjectListCtrl(parent,winId)

    for idx,columnName in enumerate(columnNames):
      listCtrl.InsertColumn(idx,columnName)

    valueTypes = set(['asset_value','threat_value','risk_class','countermeasure_value','capability','motivation','asset_type','threat_type','vulnerability_type','severity','likelihood'])
    if (dimName in valueTypes):
      if envName == '':
        parent.objts = objtFn(dimName)
      else:
        parent.objts = objtFn(dimName,envName)
      newParentObjts = {}
      listRow = 0
      for objt in parent.objts:
        parent.addObjectRow(listCtrl,listRow,objt)
        newParentObjts[objt.name()] = objt
        listRow += 1
      parent.objts = newParentObjts
    else:
      parent.objts = objtFn()

      listRow = 0
      keyNames = parent.objts.keys()
      keyNames.sort()
      for keyName in keyNames:
        objt = parent.objts[keyName]
        parent.addObjectRow(listCtrl,listRow,objt)
        listRow += 1

    for idx,columnNames in enumerate(columnNames):
      listCtrl.SetColumnWidth(idx,125)
    return listCtrl

  def buildAddDeleteCloseButtonSizer(parent,addId,deleteId,orientation=wx.VERTICAL):
    buttonSizer = wx.BoxSizer(orientation)
    addButton = wx.Button(parent,addId,"Add")
    buttonSizer.Add(addButton)
    if (parent.__class__.__name__ == 'VulnerabilitiesDialog' or parent.__class__.__name__ == 'ThreatsDialog'):
      importButton = wx.Button(parent,armid.CC_DIRECTORYIMPORT_ID,'Import')
      buttonSizer.Add(importButton)
    deleteButton = wx.Button(parent,deleteId,"Delete")
    buttonSizer.Add(deleteButton)
    closeButton = wx.Button(parent,wx.ID_CLOSE,"Close")
    buttonSizer.Add(closeButton)
    return buttonSizer

  def buildAddDeleteCloseIEButtonSizer(parent,addId,deleteId,importId,exportId,orientation=wx.VERTICAL):
    buttonSizer = wx.BoxSizer(orientation)
    addButton = wx.Button(parent,addId,"Add")
    buttonSizer.Add(addButton)
    if (parent.__class__.__name__ == 'VulnerabilitiesDialog' or parent.__class__.__name__ == 'ThreatsDialog'):
      importButton = wx.Button(parent,armid.CC_DIRECTORYIMPORT_ID,'Import')
      buttonSizer.Add(importButton)
    deleteButton = wx.Button(parent,deleteId,"Delete")
    buttonSizer.Add(deleteButton)
    importButton = wx.Button(parent,importId,"Import")
    buttonSizer.Add(importButton)
    exportButton = wx.Button(parent,exportId,"Export")
    buttonSizer.Add(exportButton)
    closeButton = wx.Button(parent,wx.ID_CLOSE,"Close")
    buttonSizer.Add(closeButton)
    return buttonSizer

  def buildCommitButtonSizer(parent,winId,isCreate):
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    commitLabel = ''
    if (isCreate):
      commitLabel = 'Create'
    else:
      commitLabel = 'Update'
    createButton = wx.Button(parent,winId,commitLabel)
    buttonSizer.Add(createButton)
    cancelButton = wx.Button(parent,wx.ID_CANCEL,"Close")
    buttonSizer.Add(cancelButton)
    return buttonSizer


