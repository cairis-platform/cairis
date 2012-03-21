#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GenerateDocumentationDialog.py $ $Id: GenerateDocumentationDialog.py 329 2010-10-31 14:59:16Z shaf $
import wx
import armid
from GenerateDocumentationPanel import GenerateDocumentationPanel

class GenerateDocumentationDialog(wx.Dialog):
  def __init__(self,parent):
    wx.Dialog.__init__(self,parent,armid.GENDOCDIALOG_ID,'Generate documentation',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX,size=(250,620))
    self.theId = -1
    self.panel = 0
    self.theDocumentType = 'Requirements'
    self.theSectionFlags = []
    self.theTypeFlags = []
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = GenerateDocumentationPanel(self)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.GENDOCPANEL_BUTTONGENERATE_ID,self.onGenerate)

  def onGenerate(self,evt):
    self.EndModal(armid.GENDOCPANEL_BUTTONGENERATE_ID)

  def documentType(self): return self.panel.documentType()
  def sectionFlags(self): return self.panel.sectionFlags()
  def typeFlags(self): return self.panel.typeFlags()
