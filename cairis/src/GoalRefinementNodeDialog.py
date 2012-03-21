#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GoalRefinementNodeDialog.py $ $Id: GoalRefinementNodeDialog.py 304 2010-07-18 21:02:32Z shaf $
import sys
import gtk
from Borg import Borg
from GoalAssociationParameters import GoalAssociationParameters
from NDImplementationDecorator import NDImplementationDecorator

class GoalRefinementNodeDialog:
  def __init__(self,objt,environmentName,builder,goalIndicator,gName,reqIndicator = False):
    self.window = builder.get_object("GoalRefinementNodeDialog")
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theEnvironmentName = environmentName
    self.decorator = NDImplementationDecorator(builder)
    self.reqIndicator = reqIndicator

    refTypes = ['and','or']
    goals = self.dbProxy.environmentGoals(self.theEnvironmentName)
    if (self.reqIndicator == True):
      refTypes = ['and']
      goals = self.dbProxy.getDimensionNames('requirement')

    self.decorator.updateComboCtrl("goalRefNameCtrl",goals,'')
    self.decorator.updateComboCtrl("goalRefinementCtrl",refTypes,'')
    self.decorator.updateButtonLabel("goalRefinementOkButton","Create")
    self.window.resize(350,200)
    self.goalIndicator = goalIndicator
    self.inputGoalName = gName

  def on_goalRefinementOkButton_clicked(self,callback_data):
    goalName = self.decorator.getComboValue("goalRefNameCtrl")
    assocType = self.decorator.getComboValue("goalRefinementCtrl")
    if (self.reqIndicator == True):
      parameters = GoalAssociationParameters(self.theEnvironmentName,self.inputGoalName,'goal','and',goalName,'requirement')
    elif (self.goalIndicator == True):
      parameters = GoalAssociationParameters(self.theEnvironmentName,goalName,'goal',assocType,self.inputGoalName,'goal')
    else:
      parameters = GoalAssociationParameters(self.theEnvironmentName,self.inputGoalName,'goal',assocType,goalName,'goal')
    self.dbProxy.addGoalAssociation(parameters)
    self.window.destroy()

  def show(self):
    self.window.show()
