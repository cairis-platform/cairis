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


import sys
import gtk
from NDImplementationDecorator import NDImplementationDecorator
from cairis.core.Borg import Borg

class RiskNodeDialog:
  def __init__(self,objt,rating,environmentName,builder):
    self.builder = builder
    self.window = self.builder.get_object("RiskNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("riskNameCtrl",objt.name())
    self.decorator.updateTextCtrl("riskThreatCtrl",objt.threat())
    self.detailsDict = {}


    self.decorator.updateTextCtrl("riskVulnerabilityCtrl",objt.vulnerability())
    self.decorator.updateTextCtrl("riskRatingCtrl",rating)
    b = Borg()
    proxy = b.dbProxy
    
    riskDetails = []
    riskScores = proxy.riskScore(objt.threat(),objt.vulnerability(),environmentName,objt.name())
    for idx,riskScore in enumerate(riskScores):
      riskDetails.append([riskScore[0],riskScore[1]])
      self.detailsDict[riskScore[0]] = riskScore[2]
    self.decorator.updateListCtrl("riskScoreCtrl",['Response','Score'],gtk.ListStore(str,str),riskDetails)
    self.defaultSize = self.window.get_size()
    detailsCtrlWindow = self.builder.get_object("riskDetailsCtrl")
    detailsCtrlWindow.hide()


  def on_riskOkButton_clicked(self,callback_data):
    self.window.destroy()

  def on_riskDetailsButton_clicked(self,callback_data):
    detailsButton = self.builder.get_object("riskDetailsButton")
    detailsCtrlWindow = self.builder.get_object("riskDetailsCtrl")
    label = detailsButton.get_label()
    if (label == 'Show Details'):
      detailsButton.set_label('Hide Details')
      detailsCtrlWindow.show()
      self.window.resize(600,525)
    else: 
      detailsButton.set_label('Show Details')
      detailsCtrlWindow.hide()
      self.window.resize(self.defaultSize[0],self.defaultSize[1])

#treeview, iter, path, user_data
  def onResponseSelected(self,widget):
    scoreCtrl = self.builder.get_object("riskScoreCtrl")
    treeselection = scoreCtrl.get_selection()
    (model, iter) = treeselection.get_selected()
    detailsBuf = self.detailsDict[model.get_value(iter, 0)]
    self.decorator.updateMLTextCtrl("riskDetailsCtrl",detailsBuf)

  def show(self):
    self.window.show()
