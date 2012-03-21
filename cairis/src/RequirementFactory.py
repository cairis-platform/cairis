#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RequirementFactory.py $ $Id: RequirementFactory.py 564 2012-03-12 17:53:00Z shaf $
from Requirement import Requirement

def build(id,label,name,description,priority,rationale,fitCriterion,originator,type,asset,version=-1):
  return Requirement(id,label,name,description,priority,rationale,fitCriterion,originator,type,asset,version)

