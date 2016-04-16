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
from cairis.core.armid import *
from DimensionListCtrl import DimensionListCtrl

class CountermeasureRoleListCtrl(DimensionListCtrl):
  def __init__(self,parent,dp,personaList):
    DimensionListCtrl.__init__(self,parent,COUNTERMEASURE_LISTROLES_ID,wx.DefaultSize,'Role','role',dp,listStyle=wx.LC_REPORT | wx.LC_SINGLE_SEL)
    self.thePersonaList = personaList

  def setEnvironment(self,environmentName):
    DimensionListCtrl.setEnvironment(self,environmentName)

  def onAddDimension(self,evt):
    dimensions = self.dbProxy.getDimensionNames(self.theDimensionTable,self.theCurrentEnvironment)
    from DimensionNameDialog import DimensionNameDialog
    dlg = DimensionNameDialog(self,self.theDimensionTable,dimensions,'Add')
    if (dlg.ShowModal() == DIMNAME_BUTTONACTION_ID):
      newRoles = dlg.dimensionNames()
      for additionalDimension in newRoles:
        idx = self.GetItemCount()
        self.InsertStringItem(idx,additionalDimension)

      tpDict = self.dbProxy.roleTasks(self.theCurrentEnvironment,newRoles)

      noOfPersonas = self.thePersonaList.GetItemCount()
      if (noOfPersonas > 0):
        currentKeys = set([])
        for x in range(noOfPersonas):
          listedTask = self.thePersonaList.GetItem(x,0)
          listedPersona = self.thePersonaList.GetItem(x,1)
          listedTuple = (listedTask.GetText(),listedPersona.GetText())
          currentKeys.add(listedTuple)
        for personaDetails in tpDict.iteritems():
          key = personaDetails[0]
          value = personaDetails[1]
          if ((key[0],key[1]) not in currentKeys):
            self.thePersonaList.InsertStringItem(0,key[0])
            self.thePersonaList.SetStringItem(0,1,key[1])
            self.thePersonaList.SetStringItem(0,2,value[0])
            self.thePersonaList.SetStringItem(0,3,value[1])
            self.thePersonaList.SetStringItem(0,4,value[2])
            self.thePersonaList.SetStringItem(0,5,value[3])
      else:
        for personaDetails in tpDict.iteritems():
          key = personaDetails[0]
          value = personaDetails[1]
          self.thePersonaList.InsertStringItem(0,key[0])
          self.thePersonaList.SetStringItem(0,1,key[1])
          self.thePersonaList.SetStringItem(0,2,value[0])
          self.thePersonaList.SetStringItem(0,3,value[1])
          self.thePersonaList.SetStringItem(0,4,value[2])
          self.thePersonaList.SetStringItem(0,5,value[3])

  def onDeleteDimension(self,evt):
    idx = self.GetFocusedItem()
    roleToGo = set([self.GetItemText(idx)])
    DimensionListCtrl.onDeleteDimension(self,evt)
    if (self.GetItemCount() > 0):
      noOfPersonas = self.thePersonaList.GetItemCount()
      if (noOfPersonas > 0):
        keysToGo = set([])
        for x in range(noOfPersonas):
           personaTask = (self.thePersonaList.GetItem(x,0)).GetText()
           personaName = (self.thePersonaList.GetItem(x,1)).GetText()
           personaObjt = self.dbProxy.dimensionObject(personaName,'persona')
           if (len( set.difference(set(personaObjt.roles(self.theCurrentEnvironment,'')),roleToGo)) == 0): 
             keysToGo.add((personaTask,personaName)) 

        for ttg,ptg in keysToGo:
          for x in range(noOfPersonas):
            if ((ttg == (self.thePersonaList.GetItem(x,0)).GetText()) and (ptg == (self.thePersonaList.GetItem(x,1)).GetText())):
              self.thePersonaList.DeleteItem(x)
    else:
      self.thePersonaList.DeleteAllItems()  

    
