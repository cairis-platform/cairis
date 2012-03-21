#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DocumentReferencePanel.py $ $Id: DocumentReferencePanel.py 527 2011-11-07 11:46:40Z shaf $
import wx
import armid
from BasePanel import BasePanel
import DocumentReference
from Borg import Borg

class DocumentReferencePanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.DOCUMENTREFERENCE_ID)
    self.theId = None
    b = Borg()
    self.dbProxy = b.dbProxy
    
  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,30),armid.DOCUMENTREFERENCE_TEXTNAME_ID),0,wx.EXPAND)

    docs = self.dbProxy.getDimensionNames('external_document')
    mainSizer.Add(self.buildComboSizerList('Document',(87,30),armid.DOCUMENTREFERENCE_COMBODOCNAME_ID,docs),0,wx.EXPAND)

    mainSizer.Add(self.buildTextSizer('Contributor',(87,30),armid.DOCUMENTREFERENCE_TEXTCONTRIBUTOR_ID),0,wx.EXPAND)

    mainSizer.Add(self.buildMLTextSizer('Excerpt',(87,30),armid.DOCUMENTREFERENCE_TEXTEXCERPT_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.DOCUMENTREFERENCE_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,objt,isReadOnly=False):
    self.theId = objt.id()
    nameCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_TEXTNAME_ID)
    docCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_COMBODOCNAME_ID)
    conCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_TEXTCONTRIBUTOR_ID)
    excCtrl = self.FindWindowById(armid.DOCUMENTREFERENCE_TEXTEXCERPT_ID)

    nameCtrl.SetValue(objt.name())
    docCtrl.SetValue(objt.document())
    conCtrl.SetValue(objt.contributor())
    excCtrl.SetValue(objt.excerpt())
