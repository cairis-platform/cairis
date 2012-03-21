#$URL$ $Id: UseCaseEnvironmentProperties.py 334 2010-11-07 19:44:00Z shaf $

from EnvironmentProperties import EnvironmentProperties
from Steps import Steps

class UseCaseEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,preCond='',steps = None,postCond=''):
    EnvironmentProperties.__init__(self,environmentName)
    self.thePreCond = preCond
    self.theSteps = steps
    self.thePostCond = postCond

  def preconditions(self): return self.thePreCond
  def steps(self): return self.theSteps
  def postconditions(self): return self.thePostCond
