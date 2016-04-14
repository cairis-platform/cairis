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


import Asset
import Attacker
import Threat
import Risk
import Mitigation
import Persona
import Scenario
import MisuseCase
import Vulnerability
import Requirement
import AssetPanel
import AttackerPanel
import ThreatPanel
import VulnerabilityPanel
import RiskPanel
import PersonaPanel
import ScenarioPanel
import MisuseCasePanel
import RequirementPanel
import ARM

def build(objt,parent):
  panel = 0
  if (objt.__class__.__name__ == 'Asset'):
    panel = AssetPanel.AssetPanel(parent)
  elif (objt.__class__.__name__ == 'Attacker'):
    panel = AttackerPanel.AttackerPanel(parent)
  elif (objt.__class__.__name__ == 'Threat'):
    panel = ThreatPanel.ThreatPanel(parent)
  elif (objt.__class__.__name__ == 'Vulnerability'):
    panel = VulnerabilityPanel.VulnerabilityPanel(parent)
  elif (objt.__class__.__name__ == 'Risk'):
    panel = RiskPanel.RiskPanel(parent)
  elif (objt.__class__.__name__ == 'Response'):
    panel = ResponsePanel.ResponsePanel(parent)
  elif (objt.__class__.__name__ == 'Countermeasure'):
    panel = CountermeasurePanel.CountermeasurePanel(parent)
  elif (objt.__class__.__name__ == 'Persona'):
    panel = PersonaPanel.PersonaPanel(parent)
  elif (objt.__class__.__name__ == 'MisuseCase'):
    panel = MisuseCasePanel.MisuseCasePanel(parent)
  elif (objt.__class__.__name__ == 'Scenario'):
    panel = ScenarioPanel.ScenarioPanel(parent)
  elif (objt.__class__.__name__ == 'Requirement'):
    panel = RequirementPanel.RequirementPanel(parent)
  else:
    raise ARM.UnknownPanelClass(str(objectId))
  panel.buildControls(False,False)
  panel.loadControls(objt,True)
  return panel
