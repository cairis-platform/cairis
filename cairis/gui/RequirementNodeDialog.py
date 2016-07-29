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

__author__ = 'Shamal Faily'

class RequirementNodeDialog:
  def __init__(self,objt,builder):
    self.window = builder.get_object("RequirementNodeDialog")
    labelCtrl = builder.get_object("requirementLabelCtrl")
    labelCtrl.set_text(str(objt.label()))
    nameCtrl = builder.get_object("requirementNameCtrl")
    nameCtrl.set_text(str(objt.name()))
    typeCtrl = builder.get_object("requirementTypeCtrl")
    typeCtrl.set_text(objt.type()) 
    priorityCtrl = builder.get_object("requirementPriorityCtrl")
    priorityCtrl.set_text(str(objt.priority())) 
    originatorCtrl = builder.get_object("requirementOriginatorCtrl")
    originatorCtrl.set_text(objt.originator()) 
    descriptionCtrl = builder.get_object("requirementDescriptionCtrl")
    descriptionBuffer = gtk.TextBuffer()
    descriptionBuffer.set_text(objt.description())
    descriptionCtrl.set_buffer(descriptionBuffer)
    rationaleCtrl = builder.get_object("requirementRationaleCtrl")
    rationaleBuffer = gtk.TextBuffer()
    rationaleBuffer.set_text(objt.rationale())
    rationaleCtrl.set_buffer(rationaleBuffer)
    fitCriterionCtrl = builder.get_object("requirementFitCriterionCtrl")
    fitCriterionBuffer = gtk.TextBuffer()
    fitCriterionBuffer.set_text(objt.fitCriterion())
    fitCriterionCtrl.set_buffer(fitCriterionBuffer)
    self.window.resize(350,500)

  def on_requirementOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
