#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TaskNodeDialog.py $ $Id: TaskNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
from Borg import Borg
from NDImplementationDecorator import NDImplementationDecorator

class TaskNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("TaskNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    taskName = objt.name()
    self.decorator.updateTextCtrl("taskNameCtrl",taskName)
    self.decorator.updateTextCtrl("taskObjectiveCtrl",objt.objective())
    self.decorator.updateMLTextCtrl("taskDependenciesCtrl",objt.dependencies(environmentName,dupProperty))

    personas  = []
    for persona in objt.personas(environmentName,dupProperty,overridingEnvironment):
      personas.append([persona[0],persona[1],persona[2],persona[3],persona[4]])
    self.decorator.updateListCtrl("taskPersonasCtrl",['Persona','Duration','Frequency','Demands','Goal conflict'],gtk.ListStore(str,str,str,str,str),personas)

    assets = []
    for asset in objt.assets(environmentName,dupProperty):
      assets.append([asset])
    self.decorator.updateListCtrl("taskAssetsCtrl",['Asset'],gtk.ListStore(str),assets)

    b = Borg()
    proxy = b.dbProxy
    self.decorator.updateTextCtrl("taskUsabilityCtrl",str(proxy.taskUsabilityScore(taskName,environmentName)))

    taskId = proxy.getDimensionId(taskName,'task')
    environmentId = proxy.getDimensionId(environmentName,'environment')
    self.decorator.updateTextCtrl("taskTaskLoadCtrl",str(proxy.taskLoad(taskId,environmentId)))
    self.decorator.updateTextCtrl("taskCountermeasureLoadCtrl",str(proxy.countermeasureLoad(taskId,environmentId)))
    self.decorator.updateMLTextCtrl("taskNarrativeCtrl",objt.narrative(environmentName,dupProperty))
    self.window.resize(350,300)

  def on_taskOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
