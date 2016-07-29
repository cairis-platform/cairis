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
from cairis.core.Borg import Borg
from NDImplementationDecorator import NDImplementationDecorator

__author__ = 'Shamal Faily'

class TaskNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("TaskNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    taskName = objt.name()
    self.decorator.updateTextCtrl("taskNameCtrl",taskName)
    self.decorator.updateTextCtrl("taskObjectiveCtrl",objt.objective())
    self.decorator.updateMLTextCtrl("taskDependenciesCtrl",objt.dependencies(environmentName,dupProperty))

    personas  = []
    for persona in objt.personas(environmentName,dupProperty,overridingEnvironment):
      personas.append([persona[0],persona[1],persona[2],persona[3],persona[4]])
    self.decorator.updateListCtrl("taskPersonasCtrl",['Persona','Duration','Frequency','Demands','Goal conflict'],gtk.ListStore(str,str,str,str,str),personas)

    assets = []
    for asset in objt.assets(environmentName,dupProperty):
      assets.append([asset])
    self.decorator.updateListCtrl("taskAssetsCtrl",['Asset'],gtk.ListStore(str),assets)

    b = Borg()
    proxy = b.dbProxy
    self.decorator.updateTextCtrl("taskUsabilityCtrl",str(proxy.taskUsabilityScore(taskName,environmentName)))

    taskId = proxy.getDimensionId(taskName,'task')
    environmentId = proxy.getDimensionId(environmentName,'environment')
    self.decorator.updateTextCtrl("taskTaskLoadCtrl",str(proxy.taskLoad(taskId,environmentId)))
    self.decorator.updateTextCtrl("taskCountermeasureLoadCtrl",str(proxy.countermeasureLoad(taskId,environmentId)))
    self.decorator.updateMLTextCtrl("taskNarrativeCtrl",objt.narrative(environmentName,dupProperty))
    self.window.resize(350,300)

  def on_taskOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
