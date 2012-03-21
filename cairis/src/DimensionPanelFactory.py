#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DimensionPanelFactory.py $ $Id: DimensionPanelFactory.py 249 2010-05-30 17:07:31Z shaf $
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
