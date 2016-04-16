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
import WidgetFactory

class ContributorEntryDialog(wx.Dialog):
  def __init__(self,parent,firstName = '',surname='',affiliation='',role=''):
    wx.Dialog.__init__(self,parent,CONTRIBUTORENTRY_ID,'Add Contributor',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(500,300))
    self.theFirstName = firstName
    self.theSurname = surname
    self.theAffiliation = affiliation
    self.theRole = role
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Firstname',(87,30),CONTRIBUTORENTRY_TEXTFIRSTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Surname',(87,30),CONTRIBUTORENTRY_TEXTSURNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Affiliation',(87,30),CONTRIBUTORENTRY_TEXTAFFILIATION_ID),0,wx.EXPAND)
    participantRoles = ['Participant','Facilitator','Scribe']
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Role',(87,30),CONTRIBUTORENTRY_COMBOROLE_ID,participantRoles),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1),1,wx.EXPAND)

    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,CONTRIBUTORENTRY_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,CONTRIBUTORENTRY_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'
    if (len(self.theFirstName) > 0):
      self.commitLabel = 'Edit'
      self.SetLabel('Edit Contributor')
      firstNameCtrl = self.FindWindowById(CONTRIBUTORENTRY_TEXTFIRSTNAME_ID)
      firstNameCtrl.SetValue(self.theFirstName)
      surnameCtrl = self.FindWindowById(CONTRIBUTORENTRY_TEXTSURNAME_ID)
      surnameCtrl.SetValue(self.theSurname)
      affiliationCtrl = self.FindWindowById(CONTRIBUTORENTRY_TEXTAFFILIATION_ID)
      affiliationCtrl.SetValue(self.theAffiliation)
      roleCtrl = self.FindWindowById(CONTRIBUTORENTRY_COMBOROLE_ID)
      roleCtrl.SetStringSelection(self.theRole)
      buttonCtrl = self.FindWindowById(CONTRIBUTORENTRY_BUTTONCOMMIT_ID)
      buttonCtrl.SetLabel('Edit')
      

  def onCommit(self,evt):
    firstNameCtrl = self.FindWindowById(CONTRIBUTORENTRY_TEXTFIRSTNAME_ID)
    surnameCtrl = self.FindWindowById(CONTRIBUTORENTRY_TEXTSURNAME_ID)
    affiliationCtrl = self.FindWindowById(CONTRIBUTORENTRY_TEXTAFFILIATION_ID)
    roleCtrl = self.FindWindowById(CONTRIBUTORENTRY_COMBOROLE_ID)

    self.theFirstName = firstNameCtrl.GetValue()
    self.theSurname = surnameCtrl.GetValue()
    self.theAffiliation = affiliationCtrl.GetValue()
    self.theRole = roleCtrl.GetStringSelection()

    if (len(self.theFirstName) == 0):
      dlg = wx.MessageDialog(self,'No firstname',self.commitLabel + ' Contributor',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theSurname) == 0):
      dlg = wx.MessageDialog(self,'No surname',self.commitLabel + ' Contributor',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theAffiliation) == 0):
      dlg = wx.MessageDialog(self,'No affiliation',self.commitLabel + ' Contributor',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theRole) == 0):
      dlg = wx.MessageDialog(self,'No role',self.commitLabel + ' Contributor',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(CONTRIBUTORENTRY_BUTTONCOMMIT_ID)

  def firstName(self): return self.theFirstName
  def surname(self): return self.theSurname
  def affiliation(self): return self.theAffiliation
  def role(self): return self.theRole
