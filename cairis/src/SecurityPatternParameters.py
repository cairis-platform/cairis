#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/SecurityPatternParameters.py $ $Id: SecurityPatternParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class SecurityPatternParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,spName,spContext,spProb,spSol,spReqs,spAssocs):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
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
