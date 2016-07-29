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

class AssetNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("AssetNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("assetNameCtrl",objt.name())
    self.decorator.updateMLTextCtrl("assetDescriptionCtrl",objt.description())
    self.decorator.updateMLTextCtrl("assetSignificanceCtrl",objt.significance())
    self.decorator.updateListCtrl("assetPropertiesCtrl",['Property','Value'],gtk.ListStore(str,str),objt.propertyList(environmentName,dupProperty,overridingEnvironment))
    self.window.resize(350,350)


  def on_assetOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
