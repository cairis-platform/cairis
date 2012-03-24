#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


import wx
from BaseDialog import BaseDialog
from Borg import Borg
import ObjectFactory
import armid
import DialogClassParameters
import DimensionNameIdentifier
import DimensionBaseDialog
import DependentsDialog
from ExposedCountermeasureDialog import ExposedCountermeasureDialog
from CharacteristicListCtrl import CharacteristicListCtrl
import os
import ARM

LIST_POS = 0
ADD_POS = 1
DELETE_POS = 2
IMPORT_POS = 3
EXPORT_POS = 4

def buildBehaviouralCharacteristicListCtrl(parent,winId,columnNames,objtFn,pName,bvName):
  listCtrl = CharacteristicListCtrl(parent,winId,pName)
  for idx,columnName in enumerate(columnNames):
    listCtrl.InsertColumn(idx,columnName)
  if (bvName != ''):
    parent.objts = objtFn(pName,bvName)
  else:
    parent.objts = objtFn(pName)
  listRow = 0
  keyNames = parent.objts.keys()
  keyNames.sort()
  for keyName in keyNames:
    objt = parent.objts[keyName]
    parent.addObjectRow(listCtrl,listRow,objt)
    listRow += 1
  listCtrl.SetColumnWidth(0,700)
  if (bvName == ''):
    listCtrl.thePersonaName = ''
  return listCtrl


class DimensionBaseDialog(BaseDialog):
  def __init__(self,parent,winId,winLabel,initSize,dimIconFile):
    BaseDialog.__init__(self,parent,winId,winLabel,initSize)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theDimensionName = DimensionNameIdentifier.dimensionName(self.__class__.__name__)
    self.selectedLabel = ""
    self.selectedIdx = -1
    dimIcon = wx.Icon(b.imageDir + '/' + dimIconFile,wx.BITMAP_TYPE_PNG)
    self.SetIcon(dimIcon)


  def buildControls(self,idList,columnList,getterFn,dimName,envName = ''):
    winSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer = wx.BoxSizer(wx.HORIZONTAL)
    idList = idList
    self.listId = idList[LIST_POS]
    addId = idList[ADD_POS]
    deleteId = idList[DELETE_POS]
    importId = -1
    exportId = -1

    if (len(idList) > 3):
      importId = idList[IMPORT_POS]
      exportId = idList[EXPORT_POS]
    orientation = wx.VERTICAL

    if (dimName == 'document_reference'):
      tcBox = wx.StaticBox(self,-1,'Document')
      comboSizer = wx.StaticBoxSizer(tcBox,wx.VERTICAL)
      docs = ['']
      docs += self.dbProxy.getDimensionNames('external_document')
      self.docCtrl = wx.ComboBox(self,armid.DOCUMENTREFERENCES_COMBOEXTERNALDOCUMENT_ID,"",choices=docs,size=wx.DefaultSize,style=wx.CB_READONLY)
      winSizer.Add(comboSizer,0,wx.EXPAND)
      comboSizer.Add(self.docCtrl,1,wx.EXPAND)
    elif (dimName == 'asset_value'):
      tcBox = wx.StaticBox(self,-1,'Environment')
      comboSizer = wx.StaticBoxSizer(tcBox,wx.VERTICAL)
      environments = self.dbProxy.getDimensionNames('environment')
      self.environmentCtrl = wx.ComboBox(self,armid.VALUETYPES_COMBOENVIRONMENT_ID,"",choices=environments,size=wx.DefaultSize,style=wx.CB_READONLY)
      winSizer.Add(comboSizer,0,wx.EXPAND)
      comboSizer.Add(self.environmentCtrl,1,wx.EXPAND)
    winSizer.Add(mainSizer,1,wx.EXPAND)

    if (dimName == 'trace'):
      mainSizer.Add(self.buildTraceListCtrl(self,self.listId,columnList,self.traces),1,wx.EXPAND)
    elif (dimName == 'behavioural_characteristic'):
      mainSizer.Add(buildBehaviouralCharacteristicListCtrl(self,self.listId,columnList,getterFn,self.theName,self.theBehaviouralVariable),1,wx.EXPAND)
    else:
      mainSizer.Add(self.buildListCtrl(self.listId,columnList,getterFn,dimName,envName),1,wx.EXPAND)

    if (importId != -1):
      mainSizer.Add(self.buildAddDeleteCloseIEButtonSizer(self,addId,deleteId,importId,exportId,orientation))
    else:
      mainSizer.Add(self.buildAddDeleteCloseButtonSizer(addId,deleteId,orientation))
    self.SetSizer(winSizer)
    wx.EVT_LIST_ITEM_SELECTED(self,self.listId,self.onItemSelected)
    wx.EVT_LIST_ITEM_DESELECTED(self,self.listId,self.onItemDeselected)
    wx.EVT_LIST_ITEM_ACTIVATED(self,self.listId,self.onUpdate)
    wx.EVT_BUTTON(self,addId,self.onAdd)
    wx.EVT_BUTTON(self,deleteId,self.onDelete)
    wx.EVT_BUTTON(self,wx.ID_CLOSE,self.onClose)

  def onItemSelected(self,evt):
    self.selectedLabel = evt.GetLabel()
    self.selectedIdx = evt.GetIndex()

  def onItemDeselected(self,evt):
    self.selectedLabel = ""

  def addObject(self,dialogClassParameters):
    dimName = 'dimension'
    try:
      dialogClass = dialogClassParameters.dclass()
      dialog = dialogClass(self,dialogClassParameters)
      if (dialog.ShowModal() == dialogClassParameters.createButtonId()):
        dialogOutParameters = dialog.parameters()
        addFn = dialogClassParameters.setter()
        objtId = addFn(dialogOutParameters)
        if (self.__class__.__name__ == 'VulnerabilitiesDialog' or self.__class__.__name__ == 'ThreatsDialog'):
          if (self.__class__.__name__ == 'VulnerabilitiesDialog'):
            dimName = 'vulnerability'
          else:
            dimName = 'threat'
          expCMs = self.dbProxy.exposedCountermeasures(dialogOutParameters)
          if (len(expCMs) > 0):
            ecDlg = ExposedCountermeasureDialog(self,expCMs)
            ecDlg.ShowModal()
            revisedExpCms = ecDlg.countermeasureEffectiveness()
            ecDlg.Destroy()
            self.dbProxy.updateCountermeasuresEffectiveness(objtId,dimName,revisedExpCms)
        self.addObjectToDialog(objtId,self.listId,dialogOutParameters)
      dialog.Destroy()
    except ARM.ARMException,errorText:
      dlg = wx.MessageDialog(self,str(errorText),'Add ' + dimName,wx.OK | wx.ICON_ERROR)
      dlg.ShowModal()
      dlg.Destroy()
      return


  def importObject(self,selectedObjt,dialogClassParameters):
    dialogClass = dialogClassParameters.dclass()
    dialog = dialogClass(self,dialogClassParameters)
    dialog.load(selectedObjt)
    if (dialog.ShowModal() == dialogClassParameters.createButtonId()):
      dialogOutParameters = dialog.parameters()
      addFn = dialogClassParameters.setter()
      objtId = addFn(dialogOutParameters)
      self.addObjectToDialog(objtId,self.listId,dialogOutParameters)
    dialog.Destroy()

  def updateObject(self,selectedObjt,dialogClassParameters):
    dialogClass = dialogClassParameters.dclass()
    dialog = dialogClass(self,dialogClassParameters)
    dialog.load(selectedObjt)
    if (dialog.ShowModal() == dialogClassParameters.createButtonId()):
      dialogOutParameters = dialog.parameters()
      updateFn = dialogClassParameters.setter()
      updateFn(dialogOutParameters)
      if (self.__class__.__name__ == 'VulnerabilitiesDialog' and self.__class__.__name__ == 'ThreatsDialog'):
        if (self.__class__.__name__ == 'VulnerabilitiesDialog'):
          dimName = 'vulnerability'
        else:
          dimName = 'threat'
        expCMs = self.dbProxy.exposedCountermeasures(dialogOutParameters)
        if (len(expCMs) > 0):
          ecDlg = ExposedCountermeasureDialog(self,expCMs)
          ecDlg.ShowModal()
          revisedExpCms = ecDlg.countermeasureEffectiveness()
          ecDlg.Destroy()
          self.dbProxy.updateCountermeasuresEffectiveness(dialogOutParameters.id(),dimName,revisedExpCms)

      self.updateDialogObject(dialogOutParameters.id(),self.listId,dialogOutParameters)
    dialog.Destroy()

  def updateDialogObject(self,objtId,listId,dialogParameters):                                                           
    if (self.__class__.__name__ == 'UseCasesDialog'):
      objtToGo = self.objts[self.listCtrl.selectedLabel()]
    elif (self.__class__.__name__ != 'DependenciesDialog' and self.__class__.__name__ != 'PersonaCharacteristicsDialog' and self.__class__.__name__ != 'TaskCharacteristicsDialog' and self.__class__.__name__ != 'BehaviouralCharacteristicsDialog'):
      objtToGo = self.objts[self.selectedLabel]
    else:
      objtToGo = self.objts[self.deprecatedLabel()]
    label = ''
    if objtToGo.__class__.__name__ == 'ClassAssociation':
      label = objtToGo.environment() + '/' + objtToGo.headAsset() + '/' + objtToGo.tailAsset() 
    elif objtToGo.__class__.__name__ == 'GoalAssociation':
      label = objtToGo.environment() + '/' + objtToGo.goal() + '/' + objtToGo.subGoal() 
    elif objtToGo.__class__.__name__ == 'Dependency':
      label = objtToGo.environment() + '/' + objtToGo.depender() + '/' + objtToGo.dependee() + '/' + objtToGo.dependency()
    elif objtToGo.__class__.__name__ == 'PersonaCharacteristic':
      label = objtToGo.persona() + '/' + objtToGo.behaviouralVariable() + '/' + objtToGo.characteristic()
    elif objtToGo.__class__.__name__ == 'TaskCharacteristic':
      label = objtToGo.task() + '/' + objtToGo.characteristic()
    else:
      label = objtToGo.name()
    del self.objts[label]

    listCtrl = self.FindWindowById(self.listId)
    listCtrl.DeleteItem(self.selectedIdx)
    updatedObjt = ObjectFactory.build(objtId,dialogParameters)
    self.addObjectRow(listCtrl,self.selectedIdx,updatedObjt)
    if ((updatedObjt.__class__.__name__ == 'ClassAssociation') or (updatedObjt.__class__.__name__ == 'GoalAssociation') or (updatedObjt.__class__.__name__ == 'Dependency') or (updatedObjt.__class__.__name__ == 'PersonaCharacteristic') or (updatedObjt.__class__.__name__ == 'TaskCharacteristic')):
      self.objts[label] = updatedObjt
    else:
      self.objts[updatedObjt.name()] = updatedObjt

  def addObjectToDialog(self,objtId,listId,dialogParameters):                                                           
    listCtrl = self.FindWindowById(self.listId)
    listRow = listCtrl.GetItemCount()
    newObjt = ObjectFactory.build(objtId,dialogParameters)

    if newObjt.__class__.__name__ == 'DocumentReference':
      selectedDocName = self.docCtrl.GetStringSelection()
      if (newObjt.document() != selectedDocName):
        return    
    
    self.addObjectRow(listCtrl,listRow,newObjt)
    if newObjt.__class__.__name__ == 'ClassAssociation':
      label = newObjt.environment() + '/' + newObjt.headAsset() + '/' + newObjt.tailAsset() 
      self.objts[label] = newObjt
    elif newObjt.__class__.__name__ == 'GoalAssociation':
      label = newObjt.environment() + '/' + newObjt.goal() + '/' + newObjt.subGoal() 
      self.objts[label] = newObjt
    elif newObjt.__class__.__name__ == 'Dependency':
      label = newObjt.environment() + '/' + newObjt.depender() + '/' + newObjt.dependee() + '/' + newObjt.dependency()
      self.objts[label] = newObjt
    elif newObjt.__class__.__name__ == 'PersonaCharacteristic':
      label = newObjt.persona() + '/' + newObjt.behaviouralVariable() + '/' + newObjt.characteristic()
      self.objts[label] = newObjt
    elif newObjt.__class__.__name__ == 'TaskCharacteristic':
      label = newObjt.task() + '/' + newObjt.characteristic()
      self.objts[label] = newObjt
    else:
      self.objts[newObjt.name()] = newObjt
      self.selectedLabel = newObjt.name()

  def deleteObject(self,errorTxt,errorLabel,deleterFn):
    if (self.__class__.__name__ == 'UseCasesDialog'):
      self.selectedLabel = self.listCtrl.selectedLabel()

    if len(self.selectedLabel) == 0:
      dlg = wx.MessageDialog(self,errorTxt,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
     
      if (self.__class__.__name__ == 'PersonaCharacteristicsDialog' or self.__class__.__name__ == 'TaskCharacteristicsDialog' or self.__class__.__name__ == 'BehaviouralCharacteristicsDialog'):
        objtToGo = self.objts[self.deprecatedLabel()]
      elif (self.__class__.__name__ != 'DependenciesDialog'):
        objtToGo = self.objts[self.selectedLabel]
      else:
        objtToGo = self.objts[self.dependencyLabel()]
      objtLabel = ''
      dbLabel = ''
      if (objtToGo.__class__.__name__ == 'ClassAssociation'):
        objtLabel = objtToGo.environment() + '/' + objtToGo.headAsset() + '/' + objtToGo.tailAsset()
      if (objtToGo.__class__.__name__ == 'Dependency'):
        objtLabel = objtToGo.environment() + '/' + objtToGo.depender() + '/' + objtToGo.dependee() + '/' + objtToGo.dependency()
      elif (objtToGo.__class__.__name__ == 'GoalAssociation'):
        objtLabel = objtToGo.environment() + '/' + objtToGo.goal() + '/' + objtToGo.subGoal()
        dbLabel = objtToGo.environment() + '/' + objtToGo.goal() + '/' + objtToGo.subGoal() + '/' + objtToGo.goalDimension() + '/' + objtToGo.subGoalDimension()
      elif (objtToGo.__class__.__name__ == 'PersonaCharacteristic'):
        objtLabel = objtToGo.persona() + '/' + objtToGo.behaviouralVariable() + '/' + objtToGo.characteristic()
      elif (objtToGo.__class__.__name__ == 'TaskCharacteristic'):
        objtLabel = objtToGo.task() + '/' + objtToGo.characteristic()
      else:
        objtLabel = objtToGo.name()

      objtId = objtToGo.id()
      if (objtToGo.__class__.__name__ == 'Dependency'):
        objtDeps = []
      else:
        objtDeps = self.dbProxy.reportDependencies(self.theDimensionName,objtId)
      if (len(objtDeps) > 0):
        dlg = DependentsDialog.DependentsDialog(self,objtDeps,self.theDimensionName)
        retValue = dlg.ShowModal()
        dlg.Destroy()
        if (retValue != armid.DEPENDENTS_BUTTONCONFIRM_ID):
          return
        else:
          self.dbProxy.deleteDependencies(objtDeps)
      del self.objts[objtLabel]
      if (objtToGo.__class__.__name__ == 'GoalAssociation'):
        deleterFn(objtId,objtToGo.goalDimension(),objtToGo.subGoalDimension())
      elif (objtToGo.__class__.__name__ == 'Dependency'):
        deleterFn(objtToGo.id(),objtToGo.dependencyType())
      elif (objtToGo.__class__.__name__ == 'ConceptReference'):
        deleterFn(objtToGo.id(),objtToGo.dimension())
      else:
        deleterFn(objtId)

      if (self.__class__.__name__ == 'UseCasesDialog'):
        self.listCtrl.DeleteItem(self.listCtrl.theSelectedIdx)
      else:
        listCtrl = self.FindWindowById(self.listId)
        listCtrl.DeleteItem(self.selectedIdx)
      self.selectedLabel = ''
    return

  def onClose(self,evt):
    self.EndModal(wx.ID_CLOSE)

  def onItemActivated(self,evt):
    selectedObjt = self.objts[self.selectedLabel]
