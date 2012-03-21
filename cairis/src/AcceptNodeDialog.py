#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AcceptNodeDialog.py $ $Id: AcceptNodeDialog.py 330 2010-10-31 15:01:28Z shaf $
import sys
import gtk
from NDImplementationDecorator import NDImplementationDecorator

class AcceptNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("AcceptNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("acceptNameCtrl",objt.name())
    self.decorator.updateTextCtrl("acceptRiskCtrl",objt.risk())
    self.decorator.updateTextCtrl("acceptCostCtrl",objt.cost(environmentName,dupProperty,overridingEnvironment))
    self.decorator.updateMLTextCtrl("acceptRationaleCtrl",objt.description(environmentName,dupProperty,overridingEnvironment))
    self.window.resize(300,300)

  def on_acceptOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
