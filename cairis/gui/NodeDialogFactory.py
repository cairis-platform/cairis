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
import gtk.glade
import os
from ThreatNodeDialog import ThreatNodeDialog
from AssetNodeDialog import AssetNodeDialog
from AssetAssociationNodeDialog import AssetAssociationNodeDialog
from GoalNodeDialog import GoalNodeDialog
from GoalRefinementNodeDialog import GoalRefinementNodeDialog
from ObstacleNodeDialog import ObstacleNodeDialog
from AttackerNodeDialog import AttackerNodeDialog
from VulnerabilityNodeDialog import VulnerabilityNodeDialog
from RoleNodeDialog import RoleNodeDialog
from RiskNodeDialog import RiskNodeDialog
from AcceptNodeDialog import AcceptNodeDialog
from TransferNodeDialog import TransferNodeDialog
from RequirementNodeDialog import RequirementNodeDialog
from NewRequirementNodeDialog import NewRequirementNodeDialog
from PersonaNodeDialog import PersonaNodeDialog
from TaskNodeDialog import TaskNodeDialog
from UseCaseNodeDialog import UseCaseNodeDialog
from MisuseCaseNodeDialog import MisuseCaseNodeDialog
from MitigateNodeDialog import MitigateNodeDialog
from CountermeasureNodeDialog import CountermeasureNodeDialog
from DomainPropertyNodeDialog import DomainPropertyNodeDialog
from AssignResponsibilityNodeDialog import AssignResponsibilityNodeDialog
from ComponentNodeDialog import ComponentNodeDialog
from cairis.core.Borg import Borg

__author__ = 'Shamal Faily'

def buildComponentModelNode(url):
  dim,objtName = url.split('#')
  b = Borg()
  proxy = b.dbProxy
  builder = gtk.Builder()
  gladeFile = b.configDir + '/imvnodes/imvnodes.xml'
  builder.add_from_file(gladeFile)

  dlg = 0
  if (dim == 'component'):
    objt = proxy.dimensionObject(objtName,dim)
    dlg = ComponentNodeDialog(objt,builder)
  else:
    return 
  dlg.show()
  builder.connect_signals(dlg)


def build(url,environmentName,newNode = False,objtName = None,assocType = None,goalIndicator = None):
  dim,objtName = url.split('#')
  b = Borg()
  proxy = b.dbProxy
  builder = gtk.Builder()
  
  gladeFile = b.configDir + '/imvnodes/imvnodes.xml'
  builder.add_from_file(gladeFile)

  objt = None
  dupProperty = None
  overridingEnvironment = None
  if (newNode == False):
    objt = proxy.dimensionObject(objtName,dim)
    dupProperty,overridingEnvironment = proxy.duplicateProperties( proxy.getDimensionId(environmentName,'environment') )
  dlg = 0
  if (dim == 'threat'):
    dlg = ThreatNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
  elif (dim == 'asset'):
    if (assocType == None):
      dlg = AssetNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
    else:
      dlg = AssetAssociationNodeDialog(objt,environmentName,builder)
  elif (dim == 'goal'):
    if (assocType == 'andrequirement'):
      dlg = NewRequirementNodeDialog(objt,environmentName,builder)
    elif (assocType == 'subrequirement'):
      dlg = GoalRefinementNodeDialog(objt,environmentName,builder,False,objtName,True)
    elif (assocType == 'assign'):
      dlg = AssignResponsibilityNodeDialog(objt,environmentName,builder,objtName)
    elif (goalIndicator == None):
      dlg = GoalNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
      dlg.parentGoal(objtName,assocType)
    elif (goalIndicator == True):
      dlg = GoalRefinementNodeDialog(objt,environmentName,builder,True,objtName)
    else:
      dlg = GoalRefinementNodeDialog(objt,environmentName,builder,False,objtName)
  elif (dim == 'obstacle'):
    dlg = ObstacleNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
    dlg.parentObstacle(objtName,assocType)
  elif (dim == 'domainproperty'):
    dlg = DomainPropertyNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
  elif (dim == 'attacker'):
    dlg = AttackerNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
  elif (dim == 'vulnerability'):
    dlg = VulnerabilityNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
  elif (dim == 'role'):
    dlg = RoleNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
  elif (dim == 'requirement'):
    if (assocType == 'assign'):
      dlg = AssignResponsibilityNodeDialog(objt,environmentName,builder,objtName,False)
    else:
      dlg = RequirementNodeDialog(objt,builder)
  elif (dim == 'persona'):
    dlg = PersonaNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
  elif (dim == 'risk'):
    rating = proxy.riskRating(objt.threat(),objt.vulnerability(),environmentName)
    dlg = RiskNodeDialog(objt,rating,environmentName,builder)
  elif (dim == 'response'):
    if (objt.responseType() == 'Accept'):
      dlg = AcceptNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
    elif (objt.responseType() == 'Transfer'):
      dlg = TransferNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
    elif (objt.responseType() == 'Mitigate'):
      dlg = MitigateNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
  elif (dim == 'task'):
    dlg = TaskNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
  elif (dim == 'usecase'):
    dlg = UseCaseNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
  elif (dim == 'misusecase'):
    dlg = MisuseCaseNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
  elif (dim == 'countermeasure'):
    dlg = CountermeasureNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
#  elif (dim == 'linkand'):
#    dlg = LinkAndNodeDialog(objt,environmentName,dupProperty,overridingEnvironment,builder)
  else:
    return 
  dlg.show()
  builder.connect_signals(dlg)
