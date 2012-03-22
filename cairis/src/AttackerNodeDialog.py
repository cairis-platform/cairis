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

class AttackerNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("AttackerNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("attackerNameCtrl",objt.name())
    roles = []
    for role in objt.roles(environmentName,dupProperty):
      roles.append([role]) 
    self.decorator.updateListCtrl("attackerRolesCtrl",['Role'],gtk.ListStore(str),roles)
    capabilities = []
    for cap,value in objt.capability(environmentName,dupProperty):
      capabilities.append([cap,value]) 
    self.decorator.updateListCtrl("attackerCapabilityCtrl",['Capability','Value'],gtk.ListStore(str,str),capabilities)
    motives = []
    for motive in objt.motives(environmentName,dupProperty):
      motives.append([motive]) 
    self.decorator.updateListCtrl("attackerMotiveCtrl",['Motive'],gtk.ListStore(str),motives)
    self.decorator.updateMLTextCtrl("attackerDescriptionCtrl",objt.description())

    self.window.resize(350,300)

  def on_attackerOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
