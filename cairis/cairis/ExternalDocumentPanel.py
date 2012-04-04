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
import WidgetFactory
import ExternalDocument

class ExternalDocumentPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.EXTERNALDOCUMENT_ID)
    self.theId = None
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.EXTERNALDOCUMENT_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Version',(87,30),armid.EXTERNALDOCUMENT_TEXTVERSION_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Date',(87,30),armid.EXTERNALDOCUMENT_TEXTDATE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Authors',(87,30),armid.EXTERNALDOCUMENT_TEXTAUTHORS_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,30),armid.EXTERNALDOCUMENT_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.EXTERNALDOCUMENT_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,objt,isReadOnly=False):
    self.theId = objt.id()
    nameCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTNAME_ID)
    versionCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTVERSION_ID)
    dateCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTDATE_ID)
    authorsCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTAUTHORS_ID)
    descCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTDESCRIPTION_ID)

    nameCtrl.SetValue(objt.name())
    versionCtrl.SetValue(objt.version())
    dateCtrl.SetValue(objt.date())
    authorsCtrl.SetValue(objt.authors())
    descCtrl.SetValue(objt.description())
