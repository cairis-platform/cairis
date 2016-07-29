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

__author__ = 'Shamal Faily'

class MitigateNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("MitigateNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("mitigateNameCtrl",objt.name())
    self.decorator.updateTextCtrl("mitigateRiskCtrl",objt.risk())
    mitType = objt.type(environmentName,dupProperty,overridingEnvironment)
    self.decorator.updateTextCtrl("mitigateTypeCtrl",mitType)

    dpFrame = builder.get_object('mitigateDetectionPointFrame')
    dmFrame = builder.get_object('mitigateDetectionMechanismsFrame')
    if (mitType == 'Detect'):
      self.decorator.updateTextCtrl("mitigateDetectionPointCtrl",objt.detectionPoint(environmentName,dupProperty,overridingEnvironment))
      dmFrame.hide()
    elif (mitType == 'React'):
      dms = []
      for dm in objt.detectionMechanisms(environmentName,dupProperty,overridingEnvironment):
        dms.append([dm])
      self.decorator.updateListCtrl("mitigateDetectionMechanismsCtrl",['Detection Mechanism'],gtk.ListStore(str),dms)
      dpFrame.hide()
    else:
      dpFrame.hide()
      dmFrame.hide()
    self.window.resize(300,300)

  def on_mitigateOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
