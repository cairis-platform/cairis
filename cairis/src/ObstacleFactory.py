#$URL$ $Id: ObstacleFactory.py 509 2011-10-30 14:27:19Z shaf $

from ObstacleParameters import ObstacleParameters
from ObstacleEnvironmentProperties import ObstacleEnvironmentProperties

def build(envName,excDetails):

  obsName = excDetails[0]
  excDim = excDetails[1]
  excVal = excDetails[2]
  excDef = excDetails[4]
  excCat = excDetails[3]
  sgRef = [(excVal,excDim,'obstruct','No','use case exception')]
  envProperties = [ObstacleEnvironmentProperties(envName,'',excDef,excCat,sgRef,[])]
  parameters = ObstacleParameters(obsName,envProperties)
  return parameters 
