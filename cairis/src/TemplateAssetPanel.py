#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TemplateAssetPanel.py $ $Id: TemplateAssetPanel.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory
import TemplateAsset
from Borg import Borg
from ValueDictionary import ValueDictionary
from AssetSummaryNotebook import AssetSummaryNotebook
from SingleEnvironmentPropertiesListCtrl import SingleEnvironmentPropertiesListCtrl

class TemplateAssetPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.TEMPLATEASSET_ID)
    self.theAssetId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.ASSET_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Short Code',(87,30),armid.ASSET_TEXTSHORTCODE_ID),0,wx.EXPAND)
    typeList = self.dbProxy.getDimensionNames('asset_type')
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Type',(87,30),armid.ASSET_COMBOTYPE_ID,typeList),0,wx.EXPAND)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.VERTICAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    nbSizer.Add(AssetSummaryNotebook(self),1,wx.EXPAND)

    values = self.dbProxy.getDimensionNames('asset_value')
    valueLookup = ValueDictionary(values)
    pBox = wx.StaticBox(self,-1)
    pSizer = wx.StaticBoxSizer(pBox,wx.VERTICAL)
    mainSizer.Add(pSizer,1,wx.EXPAND)
    self.propertiesList = SingleEnvironmentPropertiesListCtrl(self,armid.TEMPLATEASSET_LISTPROPERTIES_ID,valueLookup)
    pSizer.Add(self.propertiesList,1,wx.EXPAND)

    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.TEMPLATEASSET_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,asset,isReadOnly=False):
    self.theAssetId = asset.id()
    nameCtrl = self.FindWindowById(armid.ASSET_TEXTNAME_ID)
    nameCtrl.SetValue(asset.name())
    shortCodeCtrl = self.FindWindowById(armid.ASSET_TEXTSHORTCODE_ID)
    shortCodeCtrl.SetValue(asset.shortCode())
    typeCtrl = self.FindWindowById(armid.ASSET_COMBOTYPE_ID)
    typeCtrl.SetValue(asset.type())
    descriptionCtrl = self.FindWindowById(armid.ASSET_TEXTDESCRIPTION_ID)
    descriptionCtrl.SetValue(asset.description())
    sigCtrl = self.FindWindowById(armid.ASSET_TEXTSIGNIFICANCE_ID)
    sigCtrl.SetValue(asset.significance())
    criticalCtrl = self.FindWindowById(armid.ASSET_CHECKCRITICAL_ID)
    criticalCtrl.SetValue(asset.critical())
    if (asset.critical() == True):
      criticalRationaleCtrl = self.FindWindowById(armid.ASSET_TEXTCRITICALRATIONALE_ID)
      criticalRationaleCtrl.Enable()
      criticalRationaleCtrl.SetValue(asset.criticalRationale())
    propertiesCtrl = self.FindWindowById(armid.TEMPLATEASSET_LISTPROPERTIES_ID)
    propertiesCtrl.load(asset.confidentialityProperty(),asset.integrityProperty(),asset.availabilityProperty(),asset.accountabilityProperty())
