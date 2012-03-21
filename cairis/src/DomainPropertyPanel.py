#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DomainPropertyPanel.py $ $Id: DomainPropertyPanel.py 547 2012-01-31 23:48:48Z shaf $
import wx
import armid
from BasePanel import BasePanel
import DomainProperty
from Borg import Borg

class DomainPropertyPanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.DOMAINPROPERTY_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.DOMAINPROPERTY_TEXTNAME_ID),0,wx.EXPAND)
    typeList = ['Hypothesis','Invariant']
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),armid.DOMAINPROPERTY_COMBOTYPE_ID,typeList),0,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Originator',(87,30),armid.DOMAINPROPERTY_TEXTORIGINATOR_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildMLTextSizer('Description',(87,30),armid.DOMAINPROPERTY_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.DOMAINPROPERTY_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,dp,isReadOnly=False):
    nameCtrl = self.FindWindowById(armid.DOMAINPROPERTY_TEXTNAME_ID)
    typeCtrl = self.FindWindowById(armid.DOMAINPROPERTY_COMBOTYPE_ID)
    origCtrl = self.FindWindowById(armid.DOMAINPROPERTY_TEXTORIGINATOR_ID)
    descCtrl = self.FindWindowById(armid.DOMAINPROPERTY_TEXTDESCRIPTION_ID)
    nameCtrl.SetValue(dp.name())
    typeCtrl.SetValue(dp.type())
    origCtrl.SetValue(dp.originator())
    descCtrl.SetValue(dp.description())
