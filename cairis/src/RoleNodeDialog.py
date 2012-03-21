#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RoleNodeDialog.py $ $Id: RoleNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
import gobject
from NDImplementationDecorator import NDImplementationDecorator


class RoleNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("RoleNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("roleNameCtrl",objt.name())
    self.decorator.updateMLTextCtrl("roleDescriptionCtrl",objt.description())
    responseCosts = []
    for responseCost in objt.responses(environmentName,dupProperty,overridingEnvironment):
      responseCosts.append([responseCost[0],responseCost[1] ])
    self.decorator.updateListCtrl("roleResponseCtrl",['Response','Cost'],gtk.ListStore(str,str),responseCosts)
    cms = []
    for cm in objt.countermeasures(environmentName,dupProperty,overridingEnvironment):
      cms.append([cm[0]])
    self.decorator.updateListCtrl("roleCountermeasureCtrl",['Countermeasure'],gtk.ListStore(str),cms)


    self.window.resize(350,200)

  def on_roleOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
