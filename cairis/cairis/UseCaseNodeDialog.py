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
from Borg import Borg
from NDImplementationDecorator import NDImplementationDecorator

class UseCaseNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("UseCaseNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.theSteps = objt.steps(environmentName)
    ucName = objt.name()
    self.decorator.updateTextCtrl("usecaseNameCtrl",ucName)
    self.decorator.updateMLTextCtrl("usecaseDescriptionCtrl",objt.description())

    actors  = []
    for actor in objt.actors():
      actors.append([actor])
    self.decorator.updateListCtrl("usecaseActorsCtrl",['Actor'],gtk.ListStore(str),actors)

    self.decorator.updateMLTextCtrl("usecasePreconditionsCtrl",objt.preconditions(environmentName))

    steps = []
    for s in self.theSteps:
      steps.append([s]) 
    self.decorator.updateListCtrl("usecaseStepsCtrl",['Step'],gtk.ListStore(str),steps)

    stepExceptions = (self.theSteps[0]).exceptions()
    excs = []
    for e in stepExceptions:
      excs.append([e])
    self.decorator.updateListCtrl("usecaseExceptionCtrl",['Exception'],gtk.ListStore(str),excs)

    self.decorator.updateMLTextCtrl("usecasePostconditionsCtrl",objt.postconditions(environmentName))

    self.window.resize(350,300)

  def on_usecaseOkButton_clicked(self,callback_data):
    self.window.destroy()

  def on_usecaseStepsCtrl_row_activated(self,widget,idx,callback_data):
   stepNo = idx[0]
   print 'move_cursor:',widget,' ',stepNo
   stepExceptions = (self.theSteps[stepNo]).exceptions()
   excs = []
   for e in stepExceptions:
     excs.append([e])
   self.decorator.updateListCtrl("usecaseExceptionCtrl",['Exception'],gtk.ListStore(str),excs)
     

  def show(self):
    self.window.show()
