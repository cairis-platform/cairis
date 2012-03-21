#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SecurityPattern.py $ $Id: SecurityPattern.py 249 2010-05-30 17:07:31Z shaf $

class SecurityPattern:
  def __init__(self,spId,spName,spContext,spProb,spSol,spReqs,spAssocs):
    self.theId = spId
    self.theName = spName
    self.theContext = spContext
    self.theProblem = spProb
    self.theSolution = spSol
    self.theRequirements = spReqs
    self.theConcernAssociations = spAssocs

  def id(self): return self.theId
  def name(self): return self.theName
  def context(self): return self.theContext
  def problem(self): return self.theProblem
  def solution(self): return self.theSolution
  def requirements(self): return self.theRequirements
  def associations(self): return self.theConcernAssociations
