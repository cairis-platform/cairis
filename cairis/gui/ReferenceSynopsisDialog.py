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
from cairis.core.ARM import *
from cairis.core.Borg import Borg
from cairis.core.ReferenceSynopsis import ReferenceSynopsis
from ReferenceSynopsisPanel import ReferenceSynopsisPanel

class ReferenceSynopsisDialog(wx.Dialog):
  def __init__(self,parent,objt,charDetails = None):
    wx.Dialog.__init__(self,parent,-1,'Edit Reference Synopsis',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX,size=(475,250))
    self.theReference = objt.reference()
    self.theId = objt.id()
    self.theSynopsis = ''
    self.theDimension = ''
    self.theActorType = ''
    self.theActor = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ReferenceSynopsisPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,REFERENCESYNOPSIS_BUTTONCOMMIT_ID,self.onCommit)

    if (objt.id() == -1):
      self.theCommitVerb = 'Create'
      if (charDetails != None):
        self.SetLabel = 'Create Characteristic Synopsis'
        charType = charDetails[0]
        tpName = charDetails[1]
        if (charType == 'persona'):
          self.theActorType = 'persona'
          self.theActor = tpName
      else:
        self.SetLabel = 'Create Reference Synopsis'
      objt = ReferenceSynopsis(-1,self.theReference,self.theSynopsis,self.theDimension,self.theActorType,self.theActor)
    else:
      if (charDetails != None):
        self.SetLabel = 'Edit Characteristic Synopsis'

      self.theReference = objt.reference()
      self.theSynopsis = objt.synopsis()
      self.theDimension = objt.dimension()
      self.theActorType = objt.actorType()
      self.theActor = objt.actor()
      self.theCommitVerb = 'Edit'
    self.panel.load(objt,charDetails)
   

  def onCommit(self,evt):
    refCtrl = self.FindWindowById(REFERENCESYNOPSIS_TEXTREFNAME_ID)
    synCtrl = self.FindWindowById(REFERENCESYNOPSIS_TEXTSYNOPSIS_ID)
    dimCtrl = self.FindWindowById(REFERENCESYNOPSIS_COMBODIMENSION_ID)
    atCtrl = self.FindWindowById(REFERENCESYNOPSIS_COMBOACTORTYPE_ID)
    actorCtrl = self.FindWindowById(REFERENCESYNOPSIS_COMBOACTORNAME_ID)

    self.theReference = refCtrl.GetValue()
    self.theSynopsis = synCtrl.GetValue()
    self.theDimension = dimCtrl.GetValue()
    self.theActorType = atCtrl.GetValue()
    self.theActor = actorCtrl.GetValue()


    commitLabel = self.theCommitVerb + ' Reference Synopsis'

    if len(self.theReference) == 0:
      dlg = wx.MessageDialog(self,'Reference cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theSynopsis) == 0:
      dlg = wx.MessageDialog(self,'Synopsis cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    if len(self.theDimension) == 0:
      dlg = wx.MessageDialog(self,'Dimension cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theActorType) == 0:
      dlg = wx.MessageDialog(self,'Actor type cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif len(self.theActor) == 0:
      dlg = wx.MessageDialog(self,'Actor cannot be empty',commitLabel,wx.OK) 
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(REFERENCESYNOPSIS_BUTTONCOMMIT_ID)

  def parameters(self):
    parameters = ReferenceSynopsis(self.theId,self.theReference,self.theSynopsis,self.theDimension,self.theActorType,self.theActor)
    return parameters
