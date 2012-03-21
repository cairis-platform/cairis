#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MitigateEnvironmentProperties.py $ $Id: MitigateEnvironmentProperties.py 249 2010-05-30 17:07:31Z shaf $
from EnvironmentProperties import EnvironmentProperties

class MitigateEnvironmentProperties(EnvironmentProperties):
  def __init__(self,environmentName,type='',detPoint='',detMechs=[]):
    EnvironmentProperties.__init__(self,environmentName)
    self.theType = type
    self.theDetectionPoint = detPoint
    self.theDetectionMechanisms = detMechs

  def type(self): return self.theType
  def detectionPoint(self): return self.theDetectionPoint
  def detectionMechanisms(self): return self.theDetectionMechanisms
