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


from GoalAssociationParameters import GoalAssociationParameters
from Borg import Borg

def build(objt,domainName,mainFrame):
  reqGrid = mainFrame.requirementGrid()
  priority = objt.priority('','')
  rationale = objt.definition('','') 
  reqTxt = 'Specialise: ' + rationale
  fitCriterion = objt.fitCriterion()
  originatorName = 'Goal model analysis'
  reqType = 'Functional'
  reqId = reqGrid.AppendRequirement(reqTxt,priority,rationale,fitCriterion,originatorName,reqType)
  b = Borg()
  p = b.dbProxy
  for envProps in objt.environmentProperties():
    gp = GoalAssociationParameters(envProps.name(),objt.name(),'goal','and',reqTxt,'requirement',0,rationale)
    p.addGoalAssociation(gp)
