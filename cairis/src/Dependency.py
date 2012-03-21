#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Dependency.py $ $Id: Dependency.py 249 2010-05-30 17:07:31Z shaf $
class Dependency:
  def __init__(self,dId,envName,depender,dependee,dependencyType,dependency,rationale):
    self.theId = dId
    self.theEnvironmentName = envName
    self.theDepender = depender
    self.theDependee = dependee
    self.theDependencyType = dependencyType
    self.theDependency = dependency
    self.theRationale = rationale

  def id(self): return self.theId
  def environment(self): return self.theEnvironmentName
  def depender(self): return self.theDepender
  def dependee(self): return self.theDependee
  def dependencyType(self): return self.theDependencyType
  def dependency(self): return self.theDependency
  def rationale(self): return self.theRationale
  def __str__(self): return self.theEnvironmentName + ' / ' + self.theDepender + ' / '  + self.theDependee + ' / ' + self.theDependencyType + ' / ' + self.theDependency + ' / ' + self.theRationale
