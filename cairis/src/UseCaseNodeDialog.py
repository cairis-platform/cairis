#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TaskNodeDialog.py $ $Id: TaskNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
from Borg import Borg
from NDImplementationDecorator import NDImplementationDecorator

class UseCaseNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("UseCaseNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.theSteps = objt.steps(environmentName)
    ucName = objt.name()
    self.decorator.updateTextCtrl("usecaseNameCtrl",ucName)
    self.decorator.updateMLTextCtrl("usecaseDescriptionCtrl",objt.description())

    actors  = []
    for actor in objt.actors():
      actors.append([actor])
    self.decorator.updateListCtrl("usecaseActorsCtrl",['Actor'],gtk.ListStore(str),actors)

    self.decorator.updateMLTextCtrl("usecasePreconditionsCtrl",objt.preconditions(environmentName))

    steps = []
    for s in self.theSteps:
      steps.append([s]) 
    self.decorator.updateListCtrl("usecaseStepsCtrl",['Step'],gtk.ListStore(str),steps)

    stepExceptions = (self.theSteps[0]).exceptions()
    excs = []
    for e in stepExceptions:
      excs.append([e])
    self.decorator.updateListCtrl("usecaseExceptionCtrl",['Exception'],gtk.ListStore(str),excs)

    self.decorator.updateMLTextCtrl("usecasePostconditionsCtrl",objt.postconditions(environmentName))

    self.window.resize(350,300)

  def on_usecaseOkButton_clicked(self,callback_data):
    self.window.destroy()

  def on_usecaseStepsCtrl_row_activated(self,widget,idx,callback_data):
   stepNo = idx[0]
   print 'move_cursor:',widget,' ',stepNo
   stepExceptions = (self.theSteps[stepNo]).exceptions()
   excs = []
   for e in stepExceptions:
     excs.append([e])
   self.decorator.updateListCtrl("usecaseExceptionCtrl",['Exception'],gtk.ListStore(str),excs)
     

  def show(self):
    self.window.show()
