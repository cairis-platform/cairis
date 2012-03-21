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
