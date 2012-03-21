#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MitigateNodeDialog.py $ $Id: MitigateNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
from NDImplementationDecorator import NDImplementationDecorator

class MitigateNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("MitigateNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("mitigateNameCtrl",objt.name())
    self.decorator.updateTextCtrl("mitigateRiskCtrl",objt.risk())
    mitType = objt.type(environmentName,dupProperty,overridingEnvironment)
    self.decorator.updateTextCtrl("mitigateTypeCtrl",mitType)

    dpFrame = builder.get_object('mitigateDetectionPointFrame')
    dmFrame = builder.get_object('mitigateDetectionMechanismsFrame')
    if (mitType == 'Detect'):
      self.decorator.updateTextCtrl("mitigateDetectionPointCtrl",objt.detectionPoint(environmentName,dupProperty,overridingEnvironment))
      dmFrame.hide()
    elif (mitType == 'React'):
      dms = []
      for dm in objt.detectionMechanisms(environmentName,dupProperty,overridingEnvironment):
        dms.append([dm])
      self.decorator.updateListCtrl("mitigateDetectionMechanismsCtrl",['Detection Mechanism'],gtk.ListStore(str),dms)
      dpFrame.hide()
    else:
      dpFrame.hide()
      dmFrame.hide()
    self.window.resize(300,300)

  def on_mitigateOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
