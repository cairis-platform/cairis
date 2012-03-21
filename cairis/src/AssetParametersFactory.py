#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssetParametersFactory.py $ $Id: AssetParametersFactory.py 435 2011-03-12 22:36:56Z shaf $
from AssetParameters import AssetParameters
from AssetEnvironmentProperties import AssetEnvironmentProperties
from Response import Response
from Borg import Borg

def build(cm):
  assetName = cm.name() + ' CM'
  assetDesc = cm.description()
  assetType = cm.type()
  shortCode = 'XX'
  significanceText = 'Mitigates risk '
  b = Borg()
  proxy = b.dbProxy
  risks = proxy.mitigatedRisks(cm.id())
  significanceText += risks[0]
  assetEnvironmentProperties = []
  for cProps in cm.environmentProperties():
    assetEnvironmentProperties.append(AssetEnvironmentProperties(cProps.name(),cProps.properties(),cProps.rationale()))
  return AssetParameters(assetName,shortCode,assetDesc,significanceText,assetType,False,'',assetEnvironmentProperties)

def buildFromTemplate(assetName,assetEnvs):
  b = Borg()
  taObjt = b.dbProxy.dimensionObject(assetName,'template_asset')
  assetDesc = taObjt.description()
  assetType = taObjt.type()
  shortCode = taObjt.shortCode()
  significanceText = taObjt.significance()
  assetEnvironmentProperties = []
  secProperties = taObjt.securityProperties()
  pRationale = taObjt.rationale()
  for envName in assetEnvs:
    assetEnvironmentProperties.append(AssetEnvironmentProperties(envName,secProperties,pRationale))
  return AssetParameters(assetName,shortCode,assetDesc,significanceText,assetType,False,'',assetEnvironmentProperties)  
