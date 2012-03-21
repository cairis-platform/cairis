#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssetNodeDialog.py $ $Id: AssetNodeDialog.py 330 2010-10-31 15:01:28Z shaf $
import sys
import gtk
from NDImplementationDecorator import NDImplementationDecorator

class AssetNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("AssetNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("assetNameCtrl",objt.name())
    self.decorator.updateMLTextCtrl("assetDescriptionCtrl",objt.description())
    self.decorator.updateMLTextCtrl("assetSignificanceCtrl",objt.significance())
    self.decorator.updateListCtrl("assetPropertiesCtrl",['Property','Value'],gtk.ListStore(str,str),objt.propertyList(environmentName,dupProperty,overridingEnvironment))
    self.window.resize(350,350)


  def on_assetOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
