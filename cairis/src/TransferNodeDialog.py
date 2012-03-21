#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TransferNodeDialog.py $ $Id: TransferNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
from NDImplementationDecorator import NDImplementationDecorator

class TransferNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("TransferNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("transferNameCtrl",objt.name())
    self.decorator.updateTextCtrl("transferRiskCtrl",objt.risk())

    roles = []
    roleList = objt.roles(environmentName,dupProperty,overridingEnvironment)
    for role in roleList:
      roles.append([role[0],role[1]])
    self.decorator.updateListCtrl("transferRolesCtrl",['Role','Cost'],gtk.ListStore(str,str),roles)
    self.decorator.updateMLTextCtrl("transferDescriptionCtrl",objt.description(environmentName,dupProperty,overridingEnvironment))
    self.window.resize(300,300)

  def on_transferOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
