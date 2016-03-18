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
