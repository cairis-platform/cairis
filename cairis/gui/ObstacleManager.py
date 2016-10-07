#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


import cairis.core.ARM
from cairis.core.Borg import Borg
from cairis.core.ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from cairis.core.Obstacle import Obstacle
from cairis.core.ObstacleParameters import ObstacleParameters

__author__ = 'Shamal Faily'

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
