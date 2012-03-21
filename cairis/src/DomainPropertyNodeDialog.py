#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DomainPropertyNodeDialog.py $ $Id: DomainPropertyNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
import gobject
from NDImplementationDecorator import NDImplementationDecorator


class DomainPropertyNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("DomainPropertyNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("domainPropertyNameCtrl",objt.name())
    self.decorator.updateTextCtrl("domainPropertyTypeCtrl",objt.type())
    self.decorator.updateMLTextCtrl("domainPropertyDescriptionCtrl",objt.description())

    self.window.resize(200,200)

  def on_roleOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
