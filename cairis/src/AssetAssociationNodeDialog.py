#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssetAssociationNodeDialog.py $ $Id: AssetAssociationNodeDialog.py 330 2010-10-31 15:01:28Z shaf $
import sys
import gtk
from Borg import Borg
from ClassAssociationParameters import ClassAssociationParameters
from NDImplementationDecorator import NDImplementationDecorator

class AssetAssociationNodeDialog:
  def __init__(self,objt,environmentName,builder):
    self.window = builder.get_object("AssetAssociationNodeDialog")
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theCurrentEnvironment = environmentName
    self.theHeadName = objt.name()
    self.decorator = NDImplementationDecorator(builder)
    assets = self.dbProxy.environmentAssets(self.theCurrentEnvironment) 
    associationTypes = ['Inheritance','Association','Aggregation','Composition','Dependency']
    multiplicityTypes = ['1','*','1..*']

    self.decorator.updateComboCtrl("assetAssociationHeadAdornmentCtrl",associationTypes,'')
    self.decorator.updateComboCtrl("assetAssociationHeadNryCtrl",multiplicityTypes,'')
    self.decorator.updateComboCtrl("assetAssociationTailNryCtrl",multiplicityTypes,'')
    self.decorator.updateComboCtrl("assetAssociationTailAdornmentCtrl",associationTypes,'')
    self.decorator.updateComboCtrl("assetAssociationTailNameCtrl",assets,'')
    self.decorator.updateButtonLabel("assetAssociationOkButton","Create")

  def on_assetAssociationOkButton_clicked(self,callback_data):
    headAdornment = self.decorator.getComboValue("assetAssociationHeadAdornmentCtrl")
    headNry = self.decorator.getComboValue("assetAssociationHeadNryCtrl")
    headRole = self.decorator.getText("assetAssociationHeadRoleCtrl")
    tailRole = self.decorator.getText("assetAssociationTailRoleCtrl")
    tailNry = self.decorator.getComboValue("assetAssociationTailNryCtrl")
    tailAdornment = self.decorator.getComboValue("assetAssociationTailAdornmentCtrl")
    tailName = self.decorator.getComboValue("assetAssociationTailNameCtrl")
    parameters = ClassAssociationParameters(self.theCurrentEnvironment,self.theHeadName,'asset',tailAdornment,tailNry,tailRole,headRole,headNry,headAdornment,'asset',tailName)
    self.dbProxy.addClassAssociation(parameters)
    self.window.destroy()

  def show(self):
    self.window.show()
