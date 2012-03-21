#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ThreatNodeDialog.py $ $Id: ThreatNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
from NDImplementationDecorator import NDImplementationDecorator


class ThreatNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("ThreatNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("threatNameCtrl",objt.name())
    self.decorator.updateTextCtrl("threatTypeCtrl",objt.type())
    self.decorator.updateTextCtrl("threatLikelihoodCtrl",objt.likelihood(environmentName,dupProperty,overridingEnvironment))
    self.decorator.updateMLTextCtrl("threatMethodCtrl",objt.method())
    attackers = []
    for attacker in objt.attackers(environmentName,dupProperty):
      attackers.append([attacker])
    self.decorator.updateListCtrl("threatAttackersCtrl",['Attacker'],gtk.ListStore(str),attackers)
    assets = []
    for asset in objt.assets(environmentName,dupProperty):
      assets.append([asset])
    self.decorator.updateListCtrl("threatAssetsCtrl",['Asset'],gtk.ListStore(str),assets)
    self.decorator.updateListCtrl("threatPropertiesCtrl",['Property','Value'],gtk.ListStore(str,str),objt.propertyList(environmentName,dupProperty,overridingEnvironment))

    self.window.resize(350,350)

  def on_threatOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
