#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/LinkAndNodeDialog.py $ $Id: LinkAndNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
from NDImplementationDecorator import NDImplementationDecorator

class LinkAndNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("LinkAndNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("goalNameCtrl",objt.name())
    self.decorator.updateMLTextCtrl("goalDefinitionCtrl",objt.definition(environmentName,dupProperty))
    self.decorator.updateTextCtrl("goalCategoryCtrl",objt.category(environmentName,dupProperty))
    self.decorator.updateTextCtrl("goalPriorityCtrl",objt.priority(environmentName,dupProperty))
    self.decorator.updateMLTextCtrl("goalFitCriterionCtrl",objt.fitCriterion(environmentName,dupProperty))
    self.decorator.updateMLTextCtrl("goalIssueCtrl",objt.issue(environmentName,dupProperty))
    self.window.resize(350,600)


  def on_goalOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
