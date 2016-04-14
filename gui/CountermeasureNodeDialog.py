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
from Target import Target
from NDImplementationDecorator import NDImplementationDecorator

class CountermeasureNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("CountermeasureNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("countermeasureNameCtrl",objt.name())
    self.decorator.updateMLTextCtrl("countermeasureDescriptionCtrl",objt.description())
    self.decorator.updateTextCtrl("countermeasureCostCtrl",objt.cost(environmentName,dupProperty,overridingEnvironment))

    reqs = []
    for req in set(objt.requirements(environmentName,dupProperty,overridingEnvironment)):
      reqs.append([req])
    self.decorator.updateListCtrl("countermeasureRequirementsCtrl",['Requirement'],gtk.ListStore(str),reqs)

    targets = []
    for target in objt.targets(environmentName,dupProperty,overridingEnvironment):
      targets.append([target.name(),target.effectiveness()])
    self.decorator.updateListCtrl("countermeasureTargetsCtrl",['Target','Effectiveness'],gtk.ListStore(str,str),targets)

    self.decorator.updateListCtrl("countermeasurePropertiesCtrl",['Property','Value'],gtk.ListStore(str,str),objt.propertyList(environmentName,dupProperty,overridingEnvironment))

    roles = []
    for role in objt.roles(environmentName,dupProperty,overridingEnvironment):
      roles.append([role])
    self.decorator.updateListCtrl("countermeasureRolesCtrl",['Role'],gtk.ListStore(str),roles)

    tps  = []
    for tp in objt.personas(environmentName,dupProperty,overridingEnvironment):
      tps.append([tp[0],tp[1],tp[2],tp[3],tp[4],tp[5]])
    self.decorator.updateListCtrl("countermeasureTaskPersonasCtrl",['Task','Persona','Duration','Frequency','Demands','Goals'],gtk.ListStore(str,str,str,str,str,str),tps)


    self.window.resize(500,300)

  def on_countermeasureOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
