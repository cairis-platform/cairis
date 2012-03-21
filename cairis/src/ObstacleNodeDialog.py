#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ObstacleNodeDialog.py $ $Id: ObstacleNodeDialog.py 509 2011-10-30 14:27:19Z shaf $
import sys
import gtk
from Borg import Borg
from ObstacleParameters import ObstacleParameters
from GoalAssociationParameters import GoalAssociationParameters
from ObstacleEnvironmentProperties import ObstacleEnvironmentProperties
from NDImplementationDecorator import NDImplementationDecorator

class ObstacleNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("ObstacleNodeDialog")
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theEnvironmentName = environmentName
    self.theObstacleAssociation = None
    self.theObstacleId = -1
    self.decorator = NDImplementationDecorator(builder)
    obstacleCategories = self.dbProxy.getDimensionNames('obstacle_category_type')
    self.obstacleAssociations = []
    self.subObstacleAssociations = []
    if (objt == None):
      self.decorator.updateComboCtrl("obstacleCategoryCtrl",obstacleCategories,'')
      self.decorator.updateButtonLabel("obstacleOkButton","Create")
      self.isCreate = True
    else:
      self.theObstacleId= objt.id()
      envProperty = objt.environmentProperty(self.theEnvironmentName)
      self.obstacleAssociations = envProperty.goalRefinements()
      self.subObstacleAssociations = envProperty.subGoalRefinements()
      self.decorator.updateTextCtrl("obstacleNameCtrl",objt.name())
      self.decorator.updateComboCtrl("obstacleCategoryCtrl",obstacleCategories,objt.category(environmentName,dupProperty))
      self.decorator.updateMLTextCtrl("obstacleDefinitionCtrl",objt.definition(environmentName,dupProperty))
      self.decorator.updateButtonLabel("obstacleOkButton","Update")
      self.isCreate = False
    self.window.resize(350,600)

  def environmentProperties(self):
    obsCat = self.decorator.getComboValue("obstacleCategoryCtrl")
    obsDef = self.decorator.getMLText("obstacleDefinitionCtrl")
    envProperties = ObstacleEnvironmentProperties(self.theEnvironmentName,'',obsDef,obsCat,self.obstacleAssociations,self.subObstacleAssociations)
    return envProperties

  def newObstacleParameters(self):
    obsName = self.decorator.getText("obstacleNameCtrl")
    envProperties = self.environmentProperties()
    parameters = ObstacleParameters(obsName,[envProperties])
    parameters.setId(self.theObstacleId)
    return parameters

  def existingObstacleParameters(self):
    obsName = self.decorator.getText("obstacleNameCtrl")
    modifiedProperties = self.environmentProperties()
    envProperties = self.dbProxy.obstacleEnvironmentProperties(self.theObstacleId)
    for idx,p in enumerate(envProperties):
      if (p.name() == self.theEnvironmentName):
        envProperties[idx] = modifiedProperties
    parameters = ObstacleParameters(obsName,envProperties)
    parameters.setId(self.theObstacleId)
    return parameters

  def parentObstacle(self,obsName,assocType):
    self.theObstacleAssociation = GoalAssociationParameters(self.theEnvironmentName,obsName,'obstacle',assocType)

  def on_obstacleOkButton_clicked(self,callback_data):
    if (self.isCreate):
      parameters = self.newObstacleParameters()
      self.dbProxy.addObstacle(parameters)
      self.theObstacleAssociation.theSubGoal = parameters.name()
      self.theObstacleAssociation.theSubGoalDimension = 'obstacle'
      self.theObstacleAssociation.theAlternativeId = 0
      self.theObstacleAssociation.theRationale = ''
      self.dbProxy.addGoalAssociation(self.theObstacleAssociation)
    else:
      parameters = self.existingObstacleParameters()
      self.dbProxy.updateObstacle(parameters)
    self.window.destroy()

  def show(self):
    self.window.show()
