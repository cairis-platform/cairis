#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RequirementManager.py $ $Id: RequirementManager.py 303 2010-07-18 16:17:17Z shaf $
import ARM
from Borg import Borg
from ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from Obstacle import Obstacle
from ObstacleParameters import ObstacleParameters


class ObstacleManager:  

  def __init__(self,obsCombo,envCombo):
    b = Borg()
    self.dbProxy = b.dbProxy
    self.obsCombo = obsCombo
    self.envCombo = envCombo
    envName = self.envCombo.GetValue()
    obsName = self.obsCombo.GetValue()
    self.obstacles = self.dbProxy.getEnvironmentObstacles(obsName,envName)

  def __getitem__(self,obsId):
    return self.obstacles[obsId]

  def objects(self):
    return self.obstacles

  def environment(self):
    return self.dbProxy.environmentId

  def size(self):
    return len(self.obstacles)

  def commitChanges(self):
    envName = self.envCombo.GetValue()
    for o in self.obstacles:
      self.dbProxy.updateEnvironmentObstacle(o,envName)
        
  def add(self,idx=-1,obsName="",envName="",newDefinition="",newCategory="Vulnerability", newOriginator=""):
    envName = self.envCombo.GetValue()
    parentObsName = self.obsCombo.GetValue()

    ep = ObstacleEnvironmentProperties(envName,'',newDefinition,newCategory,[(parentObsName,'obstacle','and','No','None')])
    o = Obstacle(-1,obsName,newOriginator,[ep])
    op = ObstacleParameters(obsName,newOriginator,[ep])
    o.setId(self.dbProxy.addObstacle(op))
    if (idx != -1):
      self.obstacles.insert(idx,o)
    else:
      self.obstacles.append(o)
    return o

  def delete(self,idx):
    o = self.obstacles[idx]
    obsId = o.id()
    self.obstacles.remove(o)    
    self.dbProxy.deleteObstacle(obsId)
    return 1

  def asString(self):
    for o in self.obstacles:
      print o.asString()
