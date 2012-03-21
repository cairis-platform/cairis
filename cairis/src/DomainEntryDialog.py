#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DomainEntryDialog.py $ $Id: DomainEntryDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory
from Borg import Borg

class DomainEntryDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,armid.DOMAINENTRY_ID,'Add domain interface',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(300,300))
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theDomain = ''
    self.theConnectionDomain = ''
    self.thePhenomena = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    domList = self.dbProxy.getDimensionNames('domain')
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Domain',(87,30),armid.DOMAINENTRY_COMBODOMAIN_ID,domList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Phenomena',(87,30),armid.DOMAINENTRY_TEXTPHENOMENA_ID),0,wx.EXPAND)
    cdList = [''] + domList
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Connection Domain',(87,30),armid.DOMAINENTRY_COMBOCONNECTIONDOMAIN_ID,cdList),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.DOMAINENTRY_BUTTONCOMMIT_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.DOMAINENTRY_BUTTONCOMMIT_ID,self.onCommit)
    self.commitLabel = 'Add'

  def onCommit(self,evt):
    domainCtrl = self.FindWindowById(armid.DOMAINENTRY_COMBODOMAIN_ID)
    connectionDomainCtrl = self.FindWindowById(armid.DOMAINENTRY_COMBOCONNECTIONDOMAIN_ID)
    phenomenaCtrl = self.FindWindowById(armid.DOMAINENTRY_TEXTPHENOMENA_ID)
    self.theDomain = domainCtrl.GetValue()
    self.theConnectionDomain = connectionDomainCtrl.GetValue()
    self.thePhenomena = phenomenaCtrl.GetValue()
    if (len(self.theDomain) == 0):
      dlg = wx.MessageDialog(self,'No domain','Add domain interface',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    if (len(self.thePhenomena) == 0):
      dlg = wx.MessageDialog(self,'No phenomena','Add domain interface',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.DOMAINENTRY_BUTTONCOMMIT_ID)

  def domain(self): return self.theDomain
  def phenomena(self): return self.thePhenomena
  def connectionDomain(self): return self.theConnectionDomain
