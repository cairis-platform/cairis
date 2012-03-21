#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ObstacleParameters.py $ $Id: ObstacleParameters.py 499 2011-10-27 15:43:45Z shaf $
import ObjectCreationParameters

class ObstacleParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,obsName,obsOrig,properties):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = obsName
    self.theOriginator = obsOrig
    self.theEnvironmentProperties = properties

  def name(self): return self.theName
  def originator(self): return self.theOriginator
  def environmentProperties(self): return self.theEnvironmentProperties
