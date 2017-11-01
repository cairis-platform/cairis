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

from . import ObjectValidator

class ComponentView(ObjectValidator.ObjectValidator):
  def __init__(self,cvId,cvName,cvSyn,cvComs,cvCons,asm = [0,0,0]):
    ObjectValidator.ObjectValidator.__init__(self)
    self.theId = cvId
    self.theName = cvName
    self.theSynopsis = cvSyn
    self.theComponents = cvComs
    self.theConnectors = cvCons
    self.theAttackSurfaceMetric = asm

  def id(self): return self.theId
  def name(self): return self.theName
  def synopsis(self): return self.theSynopsis
  def components(self): return self.theComponents
  def connectors(self): return self.theConnectors
  def attackSurfaceMetric(self): return self.theAttackSurfaceMetric
