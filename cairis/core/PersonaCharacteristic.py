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

__author__ = 'Shamal Faily'

class PersonaCharacteristic:
  def __init__(self,pcId,pName,modQual,vName,cDesc,pcGrounds,pcWarrant,pcBacking,pcRebuttal):
    self.theId = pcId
    self.thePersonaName = pName
    self.theModQual = modQual
    self.theVariable = vName
    self.theName = cDesc
    self.theGrounds = pcGrounds
    self.theWarrant = pcWarrant
    self.theBacking = pcBacking
    self.theRebuttal = pcRebuttal
       

  def id(self): return self.theId
  def persona(self): return self.thePersonaName
  def qualifier(self): return self.theModQual
  def behaviouralVariable(self): return self.theVariable
  def characteristic(self): return self.theName
  def name(self): return self.theName
  def grounds(self): return self.theGrounds
  def warrant(self): return self.theWarrant
  def backing(self): return self.theBacking
  def rebuttal(self): return self.theRebuttal
