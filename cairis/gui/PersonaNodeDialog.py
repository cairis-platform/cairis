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

class PersonaNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("PersonaNodeDialog")
    self.decorator = NDImplementationDecorator(builder) 
    self.decorator.updateTextCtrl("personaNameCtrl",objt.name())
    self.decorator.updateMLTextCtrl("personaActivitiesCtrl",objt.activities())
    self.decorator.updateMLTextCtrl("personaAttitudesCtrl",objt.attitudes())
    self.decorator.updateMLTextCtrl("personaAptitudesCtrl",objt.aptitudes())
    self.decorator.updateMLTextCtrl("personaMotivationsCtrl",objt.motivations())
    self.decorator.updateMLTextCtrl("personaSkillsCtrl",objt.skills())
    self.decorator.updateImageCtrl("personaImageCtrl",objt.image())

    self.decorator.updateTextCtrl("personaDirectCtrl",objt.directFlag(environmentName,dupProperty))
    roles = []
    for role in objt.roles(environmentName,dupProperty):
      roles.append([role])
    self.decorator.updateListCtrl("personaRolesCtrl",['Role'],gtk.ListStore(str),roles)
    self.decorator.updateMLTextCtrl("personaNarrativeCtrl",objt.narrative(environmentName,dupProperty))

    self.window.resize(400,400)

  def on_personaOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
