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
import wx.lib.imagebrowser
from BVNarrativeTextCtrl import BVNarrativeTextCtrl

__author__ = 'Shamal Faily'

class SummaryPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    activitiesBox = wx.StaticBox(self,-1,'')
    activitiesSizer = wx.StaticBoxSizer(activitiesBox,wx.HORIZONTAL)
    topSizer.Add(activitiesSizer,1,wx.EXPAND)
    activitiesCtrl = BVNarrativeTextCtrl(self,PERSONA_TEXTACTIVITIES_ID)
    activitiesCtrl.theBehaviouralVariable = 'Activites'
    activitiesSizer.Add(activitiesCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class AttitudesPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    attitudesBox = wx.StaticBox(self,-1,'')
    attitudesSizer = wx.StaticBoxSizer(attitudesBox,wx.HORIZONTAL)
    topSizer.Add(attitudesSizer,1,wx.EXPAND)
    attitudesCtrl = BVNarrativeTextCtrl(self,PERSONA_TEXTATTITUDES_ID)
    attitudesCtrl.theBehaviouralVariable = 'Attitudes'
    attitudesSizer.Add(attitudesCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class AptitudesPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    aptitudesBox = wx.StaticBox(self,-1,'')
    aptitudesSizer = wx.StaticBoxSizer(aptitudesBox,wx.HORIZONTAL)
    topSizer.Add(aptitudesSizer,1,wx.EXPAND)
    aptitudesCtrl = BVNarrativeTextCtrl(self,PERSONA_TEXTAPTITUDES_ID)
    aptitudesCtrl.theBehaviouralVariable = 'Aptitudes'
    aptitudesSizer.Add(aptitudesCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class MotivationsPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    mBox = wx.StaticBox(self,-1,'')
    mSizer = wx.StaticBoxSizer(mBox,wx.HORIZONTAL)
    topSizer.Add(mSizer,1,wx.EXPAND)
    mCtrl = BVNarrativeTextCtrl(self,PERSONA_TEXTMOTIVATIONS_ID)
    mCtrl.theBehaviouralVariable = 'Motivations'
    mSizer.Add(mCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class SkillsPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    sBox = wx.StaticBox(self,-1,'')
    sSizer = wx.StaticBoxSizer(sBox,wx.HORIZONTAL)
    topSizer.Add(sSizer,1,wx.EXPAND)
    sCtrl = BVNarrativeTextCtrl(self,PERSONA_TEXTSKILLS_ID)
    sCtrl.theBehaviouralVariable = 'Skills'
    sSizer.Add(sCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class IntrinsicPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    sBox = wx.StaticBox(self,-1,'')
    sSizer = wx.StaticBoxSizer(sBox,wx.HORIZONTAL)
    topSizer.Add(sSizer,1,wx.EXPAND)
    sCtrl = BVNarrativeTextCtrl(self,PERSONA_TEXTINTRINSIC_ID)
    sCtrl.theBehaviouralVariable = 'Intrinsic'
    sSizer.Add(sCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class ContextualPage(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    sBox = wx.StaticBox(self,-1,'')
    sSizer = wx.StaticBoxSizer(sBox,wx.HORIZONTAL)
    topSizer.Add(sSizer,1,wx.EXPAND)
    sCtrl = BVNarrativeTextCtrl(self,PERSONA_TEXTCONTEXTUAL_ID)
    sCtrl.theBehaviouralVariable = 'Contextual'
    sSizer.Add(sCtrl,1,wx.EXPAND)
    self.SetSizer(topSizer)

class SummaryDetailsNotebook(wx.Notebook):
  def __init__(self,parent):
    wx.Notebook.__init__(self,parent,PERSONA_NOTEBOOKSUMMARY_ID)
    p1 = SummaryPage(self)
    p2 = AttitudesPage(self)
    p3 = AptitudesPage(self)
    p4 = MotivationsPage(self)
    p5 = SkillsPage(self)
    p6 = IntrinsicPage(self)
    p7 = ContextualPage(self)
    self.AddPage(p1,'Activities')
    self.AddPage(p2,'Attitudes')
    self.AddPage(p3,'Aptitudes')
    self.AddPage(p4,'Motivations')
    self.AddPage(p5,'Skills')
    self.AddPage(p6,'Intrinsic')
    self.AddPage(p7,'Contextual')
