#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DependencyParameters.py $ $Id: DependencyParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class DependencyParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,envName,depender,dependee,dependencyType,dependency,rationale):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theEnvironmentName = envName
    self.theDepender = depender
    self.theDependee = dependee
    self.theDependencyType = dependencyType
    self.theDependency = dependency
    self.theRationale = rationale

  def environment(self): return self.theEnvironmentName
  def depender(self): return self.theDepender
  def dependee(self): return self.theDependee
  def dependencyType(self): return self.theDependencyType
  def dependency(self): return self.theDependency
  def rationale(self): return self.theRationale
