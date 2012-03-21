#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/GenerateDocumentationPanel.py $ $Id: GenerateDocumentationPanel.py 329 2010-10-31 14:59:16Z shaf $
import wx
from RequirementsDocumentationPanel import RequirementsDocumentationPanel
from PersonasDocumentationPanel import PersonasDocumentationPanel
import armid

class GenerateDocumentationPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.GENDOCPANEL_ID)
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    docTypeBox = wx.StaticBox(self,-1,'Type')
    docTypeSizer = wx.StaticBoxSizer(docTypeBox,wx.HORIZONTAL)
    self.docTypeCtrl = wx.ComboBox(self,armid.GENDOCPANEL_COMBODOCTYPE_ID,choices=['Requirements','Personas'], size=wx.DefaultSize, style=wx.CB_READONLY)
    self.docTypeCtrl.SetSelection(0)
    docTypeSizer.Add(self.docTypeCtrl,1,wx.EXPAND)
    mainSizer.Add(docTypeSizer,0,wx.EXPAND)

    checkBox = wx.StaticBox(self,-1,'Sections')
    self.checkSizer = wx.StaticBoxSizer(checkBox,wx.VERTICAL)
    mainSizer.Add(self.checkSizer,0,wx.EXPAND)

    self.reqPanel = RequirementsDocumentationPanel(self)
    self.perPanel = PersonasDocumentationPanel(self)
    self.checkSizer.Add(self.reqPanel,1,wx.EXPAND)
    self.checkSizer.Add(self.perPanel,1,wx.EXPAND)
    self.checkSizer.Show(0,True,True)
    self.checkSizer.Hide(1,True)

    otBox = wx.StaticBox(self,-1,'Output Type')
    otSizer = wx.StaticBoxSizer(otBox,wx.VERTICAL)
    mainSizer.Add(otSizer,0,wx.EXPAND)

    self.htmlCheck = wx.CheckBox(self,armid.DOCOPT_HTML_ID,'HTML')
    self.htmlCheck.SetValue(True)
    otSizer.Add(self.htmlCheck,0,wx.EXPAND)

    self.rtfCheck = wx.CheckBox(self,armid.DOCOPT_RTF_ID,'RTF')
    self.rtfCheck.SetValue(False)
    otSizer.Add(self.rtfCheck,0,wx.EXPAND)

    self.pdfCheck = wx.CheckBox(self,armid.DOCOPT_PDF_ID,'PDF')
    self.pdfCheck.SetValue(False)
    otSizer.Add(self.pdfCheck,0,wx.EXPAND)

    mainSizer.Add(wx.StaticText(self,-1,''),1,wx.EXPAND)

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.ALIGN_CENTER)

    buttonSizer.Add(wx.Button(self,armid.GENDOCPANEL_BUTTONGENERATE_ID,'Generate'))
    buttonSizer.Add(wx.Button(self,wx.ID_CANCEL,'Cancel'))

    self.SetSizer(mainSizer)
    self.docTypeCtrl.Bind(wx.EVT_COMBOBOX,self.onDocTypeChange)


  def onDocTypeChange(self,evt):
    if (self.docTypeCtrl.GetStringSelection() == 'Requirements'):
      self.checkSizer.Show(0,True,True)
      self.checkSizer.Show(1,False,True)
    else:
      self.checkSizer.Show(0,False,True)
      self.checkSizer.Show(1,True,True)
    self.checkSizer.Layout()

  def sectionFlags(self):
    if self.docTypeCtrl.GetStringSelection() == 'Requirements':
      return self.reqPanel.sectionFlags()
    else:
      return self.perPanel.sectionFlags()

  def typeFlags(self):
    flags = [
      self.htmlCheck.GetValue(),
      self.rtfCheck.GetValue(),
      self.pdfCheck.GetValue()]
    return flags  

  def documentType(self):
    return self.docTypeCtrl.GetStringSelection()
