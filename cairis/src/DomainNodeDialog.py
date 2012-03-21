#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DomainNodeDialog.py $ $Id: DomainNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
from NDImplementationDecorator import NDImplementationDecorator

class DomainNodeDialog:
  def __init__(self,objt,builder):
    self.window = builder.get_object("DomainNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("domainNameCtrl",objt.name())
    self.decorator.updateTextCtrl("domainTypeCtrl",objt.type())
    self.decorator.updateTextCtrl("domainShortCodeCtrl",objt.shortCode())
    self.decorator.updateMLTextCtrl("domainDescriptionCtrl",objt.description())
    self.window.resize(350,350)


  def on_assetOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
