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

class ComponentNodeDialog:
  def __init__(self,objt,builder):
    self.window = builder.get_object("ComponentNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    componentName = objt.name()
    self.decorator.updateTextCtrl("componentNameCtrl",componentName)
    self.decorator.updateMLTextCtrl("componentDescriptionCtrl",objt.description())

    cifs  = []
    for cif in objt.interfaces():
      cifs.append([cif[0],cif[1]])
    self.decorator.updateListCtrl("componentInterfacesCtrl",['Name','Type'],gtk.ListStore(str,str),cifs)

    cStructure = []
    for csRow  in objt.structure():
      cStructure.append([csRow[0],csRow[1],csRow[2],csRow[3],csRow[4],csRow[5],csRow[6],csRow[7],csRow[8],csRow[9]])
    self.decorator.updateListCtrl("componentStructureCtrl",['Head Asset','Type','Nav','Nry','Role','Tail Role','Tail Nry','Tail Nav','Tail Type','Tail Asset'],gtk.ListStore(str,str,str,str,str,str,str,str,str,str),cStructure)

    reqs  = []
    for req in objt.requirements():
      reqs.append([req])
    self.decorator.updateListCtrl("componentRequirementsCtrl",['Name'],gtk.ListStore(str),reqs)

    self.window.resize(350,300)

  def on_componentOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
