#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/NewRequirementNodeDialog.py $ $Id: NewRequirementNodeDialog.py 329 2010-10-31 14:59:16Z shaf $
import sys
import gtk
from Borg import Borg
import RequirementFactory
from Requirement import Requirement
from GoalAssociationParameters import GoalAssociationParameters
from NDImplementationDecorator import NDImplementationDecorator

class NewRequirementNodeDialog:
  def __init__(self,objt,environmentName,builder):
    self.window = builder.get_object("NewRequirementNodeDialog")
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theGoalName = objt.name()
    self.theEnvironmentName = environmentName
    self.theGoalAssociation = None
    self.decorator = NDImplementationDecorator(builder)
    reqTypes = self.dbProxy.getDimensionNames('requirement_type')
    priorityTypes = ['1','2','3']
    reqAssets = self.dbProxy.environmentAssets(self.theEnvironmentName)
    self.goalAssociations = []
    self.subGoalAssociations= []
    self.decorator.updateComboCtrl("newRequirementTypeCtrl",reqTypes,'')
    self.decorator.updateComboCtrl("requirementAssetCtrl",reqAssets,'')
    self.decorator.updateComboCtrl("newRequirementPriorityCtrl",priorityTypes,'')
    self.window.resize(350,600)


  def requirementParameters(self):
    reqType = self.decorator.getComboValue("newRequirementTypeCtrl")
    reqPri = self.decorator.getComboValue("newRequirementPriorityCtrl")
    reqDesc = self.decorator.getMLText("newRequirementDescriptionCtrl")
    reqRat = self.decorator.getMLText("newRequirementRationaleCtrl")
    reqFC = self.decorator.getMLText("newRequirementFitCriterionCtrl")
    reqOrig = self.decorator.getMLText("newRequirementOriginatorCtrl")
    self.theAssetName = self.decorator.getComboValue("requirementAssetCtrl")
    completeReqLabel = self.dbProxy.lastRequirementLabel(self.theAssetName)
    reqAsset,reqLabel = completeReqLabel.split('-')
    reqId = self.dbProxy.newId()
    reqLabel = int(reqLabel)
    reqLabel += 1
    r = RequirementFactory.build(reqId,reqLabel,reqDesc,reqPri,reqRat,reqFC,reqOrig,reqType,self.theAssetName)
    return r

  def requirementAsset(self):
    return self.theAssetName

  def on_newRequirementOkButton_clicked(self,callback_data):
    req = self.requirementParameters()
    self.dbProxy.addRequirement(req,self.theAssetName,True)
    reqLabel = self.dbProxy.lastRequirementLabel(self.theAssetName)
    self.theGoalAssociation = GoalAssociationParameters(self.theEnvironmentName,self.theGoalName,'goal','and',reqLabel,'requirement',)
    self.dbProxy.addGoalAssociation(self.theGoalAssociation)
    self.window.destroy()

  def show(self):
    self.window.show()
