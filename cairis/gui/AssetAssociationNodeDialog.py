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
from cairis.core.ClassAssociationParameters import ClassAssociationParameters
from NDImplementationDecorator import NDImplementationDecorator

__author__ = 'Shamal Faily'

class AssetAssociationNodeDialog:
  def __init__(self,objt,environmentName,builder):
    self.window = builder.get_object("AssetAssociationNodeDialog")
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theCurrentEnvironment = environmentName
    self.theHeadName = objt.name()
    self.decorator = NDImplementationDecorator(builder)
    assets = self.dbProxy.environmentAssets(self.theCurrentEnvironment) 
    associationTypes = ['Inheritance','Association','Aggregation','Composition','Dependency']
    multiplicityTypes = ['1','*','1..*']

    self.decorator.updateComboCtrl("assetAssociationHeadAdornmentCtrl",associationTypes,'')
    self.decorator.updateComboCtrl("assetAssociationHeadNryCtrl",multiplicityTypes,'')
    self.decorator.updateComboCtrl("assetAssociationTailNryCtrl",multiplicityTypes,'')
    self.decorator.updateComboCtrl("assetAssociationTailAdornmentCtrl",associationTypes,'')
    self.decorator.updateComboCtrl("assetAssociationTailNameCtrl",assets,'')
    self.decorator.updateButtonLabel("assetAssociationOkButton","Create")

  def on_assetAssociationOkButton_clicked(self,callback_data):
    headAdornment = self.decorator.getComboValue("assetAssociationHeadAdornmentCtrl")
    headNry = self.decorator.getComboValue("assetAssociationHeadNryCtrl")
    headRole = self.decorator.getText("assetAssociationHeadRoleCtrl")
    tailRole = self.decorator.getText("assetAssociationTailRoleCtrl")
    tailNry = self.decorator.getComboValue("assetAssociationTailNryCtrl")
    tailAdornment = self.decorator.getComboValue("assetAssociationTailAdornmentCtrl")
    tailName = self.decorator.getComboValue("assetAssociationTailNameCtrl")
    parameters = ClassAssociationParameters(self.theCurrentEnvironment,self.theHeadName,'asset',tailAdornment,tailNry,tailRole,headRole,headNry,headAdornment,'asset',tailName)
    self.dbProxy.addClassAssociation(parameters)
    self.window.destroy()

  def show(self):
    self.window.show()
