#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AttackerNodeDialog.py $ $Id: AttackerNodeDialog.py 330 2010-10-31 15:01:28Z shaf $
import sys
import gtk
from NDImplementationDecorator import NDImplementationDecorator

class AttackerNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("AttackerNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("attackerNameCtrl",objt.name())
    roles = []
    for role in objt.roles(environmentName,dupProperty):
      roles.append([role]) 
    self.decorator.updateListCtrl("attackerRolesCtrl",['Role'],gtk.ListStore(str),roles)
    capabilities = []
    for cap,value in objt.capability(environmentName,dupProperty):
      capabilities.append([cap,value]) 
    self.decorator.updateListCtrl("attackerCapabilityCtrl",['Capability','Value'],gtk.ListStore(str,str),capabilities)
    motives = []
    for motive in objt.motives(environmentName,dupProperty):
      motives.append([motive]) 
    self.decorator.updateListCtrl("attackerMotiveCtrl",['Motive'],gtk.ListStore(str),motives)
    self.decorator.updateMLTextCtrl("attackerDescriptionCtrl",objt.description())

    self.window.resize(350,300)

  def on_attackerOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
