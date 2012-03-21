#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssignResponsibilityNodeDialog.py $ $Id: AssignResponsibilityNodeDialog.py 399 2011-01-07 21:19:21Z shaf $
import sys
import gtk
from Borg import Borg
from GoalAssociationParameters import GoalAssociationParameters
from NDImplementationDecorator import NDImplementationDecorator

class AssignResponsibilityNodeDialog:
  def __init__(self,objt,environmentName,builder,goalName,isGoal = True):
    self.window = builder.get_object("AssignResponsibilityNodeDialog")
    b = Borg()
    self.isGoalIndicator = isGoal
    self.dbProxy = b.dbProxy
    self.theEnvironmentName = environmentName
    self.theGoalName = goalName
    self.decorator = NDImplementationDecorator(builder)
    self.theObjtId = objt.id()

    roles = self.dbProxy.getDimensionNames('role')
    self.decorator.updateComboCtrl("roleRespNameCtrl",roles,'')
    self.window.resize(350,200)

  def on_roleResponsibilityOkButton_clicked(self,callback_data):
    roleName = self.decorator.getComboValue("roleRespNameCtrl")
    if (self.isGoalIndicator == False):
      roleId = self.dbProxy.getDimensionId(roleName,'role')
      self.dbProxy.addTrace('requirement_role',self.theObjtId,roleId)
    else: 
      goalDim = 'goal'
      if (self.isGoalIndicator == False):
        goalDim = 'requirement'
      parameters = GoalAssociationParameters(self.theEnvironmentName,self.theGoalName,goalDim,'responsible',roleName,'role')
      self.dbProxy.addGoalAssociation(parameters)
    self.window.destroy()

  def show(self):
    self.window.show()
