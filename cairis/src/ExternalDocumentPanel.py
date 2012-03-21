#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ExternalDocumentPanel.py $ $Id: ExternalDocumentPanel.py 419 2011-01-25 21:34:13Z shaf $
import wx
import armid
import WidgetFactory
import ExternalDocument

class ExternalDocumentPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.EXTERNALDOCUMENT_ID)
    self.theId = None
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Name',(87,30),armid.EXTERNALDOCUMENT_TEXTNAME_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Version',(87,30),armid.EXTERNALDOCUMENT_TEXTVERSION_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Date',(87,30),armid.EXTERNALDOCUMENT_TEXTDATE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Authors',(87,30),armid.EXTERNALDOCUMENT_TEXTAUTHORS_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,30),armid.EXTERNALDOCUMENT_TEXTDESCRIPTION_ID),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildCommitButtonSizer(self,armid.EXTERNALDOCUMENT_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,objt,isReadOnly=False):
    self.theId = objt.id()
    nameCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTNAME_ID)
    versionCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTVERSION_ID)
    dateCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTDATE_ID)
    authorsCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTAUTHORS_ID)
    descCtrl = self.FindWindowById(armid.EXTERNALDOCUMENT_TEXTDESCRIPTION_ID)

    nameCtrl.SetValue(objt.name())
    versionCtrl.SetValue(objt.version())
    dateCtrl.SetValue(objt.date())
    authorsCtrl.SetValue(objt.authors())
    descCtrl.SetValue(objt.description())
