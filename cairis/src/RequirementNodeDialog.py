#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RequirementNodeDialog.py $ $Id: RequirementNodeDialog.py 570 2012-03-14 18:31:37Z shaf $
import sys
import gtk

class RequirementNodeDialog:
  def __init__(self,objt,builder):
    self.window = builder.get_object("RequirementNodeDialog")
    labelCtrl = builder.get_object("requirementLabelCtrl")
    labelCtrl.set_text(str(objt.label()))
    nameCtrl = builder.get_object("requirementNameCtrl")
    nameCtrl.set_text(str(objt.name()))
    typeCtrl = builder.get_object("requirementTypeCtrl")
    typeCtrl.set_text(objt.type()) 
    priorityCtrl = builder.get_object("requirementPriorityCtrl")
    priorityCtrl.set_text(str(objt.priority())) 
    originatorCtrl = builder.get_object("requirementOriginatorCtrl")
    originatorCtrl.set_text(objt.originator()) 
    descriptionCtrl = builder.get_object("requirementDescriptionCtrl")
    descriptionBuffer = gtk.TextBuffer()
    descriptionBuffer.set_text(objt.description())
    descriptionCtrl.set_buffer(descriptionBuffer)
    rationaleCtrl = builder.get_object("requirementRationaleCtrl")
    rationaleBuffer = gtk.TextBuffer()
    rationaleBuffer.set_text(objt.rationale())
    rationaleCtrl.set_buffer(rationaleBuffer)
    fitCriterionCtrl = builder.get_object("requirementFitCriterionCtrl")
    fitCriterionBuffer = gtk.TextBuffer()
    fitCriterionBuffer.set_text(objt.fitCriterion())
    fitCriterionCtrl.set_buffer(fitCriterionBuffer)
    self.window.resize(350,500)

  def on_requirementOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
