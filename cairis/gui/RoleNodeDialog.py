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
import gobject
from NDImplementationDecorator import NDImplementationDecorator

__author__ = 'Shamal Faily'

class RoleNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("RoleNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("roleNameCtrl",objt.name())
    self.decorator.updateMLTextCtrl("roleDescriptionCtrl",objt.description())
    responseCosts = []
    for responseCost in objt.responses(environmentName,dupProperty,overridingEnvironment):
      responseCosts.append([responseCost[0],responseCost[1] ])
    self.decorator.updateListCtrl("roleResponseCtrl",['Response','Cost'],gtk.ListStore(str,str),responseCosts)
    cms = []
    for cm in objt.countermeasures(environmentName,dupProperty,overridingEnvironment):
      cms.append([cm[0]])
    self.decorator.updateListCtrl("roleCountermeasureCtrl",['Countermeasure'],gtk.ListStore(str),cms)


    self.window.resize(350,200)

  def on_roleOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
