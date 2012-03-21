#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/CountermeasurePanel.py $ $Id: CountermeasurePanel.py 527 2011-11-07 11:46:40Z shaf $
import wx
import ARM
import armid
from BasePanel import BasePanel
from Borg import Borg
from CountermeasureParameters import CountermeasureParameters
from CountermeasureEnvironmentPanel import CountermeasureEnvironmentPanel

class CountermeasurePanel(BasePanel):
  def __init__(self,parent):
    BasePanel.__init__(self,parent,armid.COUNTERMEASURE_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theCountermeasureName = ''
    self.theCountermeasureDescription = ''
    self.theCountermeasureType = ''
    self.theCommitVerb = 'Create'
    self.environmentPanel = CountermeasureEnvironmentPanel(self,self.dbProxy)
    self.theEnvironmentProperties = []

  def buildControls(self,isCreate,isUpdateable = True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(self.buildTextSizer('Name',(87,60),armid.COUNTERMEASURE_TEXTNAME_ID),0,wx.EXPAND)
    typeList = ['Information','Systems','Software','Hardware','People']
    mainSizer.Add(self.buildComboSizerList('Type',(87,30),armid.COUNTERMEASURE_COMBOTYPE_ID,typeList),0,wx.EXPAND)
    mainSizer.Add(self.buildMLTextSizer('Description',(87,60),armid.COUNTERMEASURE_TEXTDESCRIPTION_ID),0,wx.EXPAND)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.COUNTERMEASURE_BUTTONCOMMIT_ID,isCreate),0,wx.CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,countermeasure,isReadOnly = False):
    nameCtrl = self.FindWindowById(armid.COUNTERMEASURE_TEXTNAME_ID)
    descriptionCtrl = self.FindWindowById(armid.COUNTERMEASURE_TEXTDESCRIPTION_ID)
    nameCtrl.SetValue(countermeasure.name())
    descriptionCtrl.SetValue(countermeasure.description())
    typeCtrl = self.FindWindowById(armid.COUNTERMEASURE_COMBOTYPE_ID)
    typeCtrl.SetValue(countermeasure.type())

    self.environmentPanel.loadControls(countermeasure)
    self.theCommitVerb = 'Edit'

  def commit(self):
    commitLabel = self.theCommitVerb + ' countermeasure'
    nameCtrl = self.FindWindowById(armid.COUNTERMEASURE_TEXTNAME_ID)
    descriptionCtrl = self.FindWindowById(armid.COUNTERMEASURE_TEXTDESCRIPTION_ID)
    typeCtrl = self.FindWindowById(armid.COUNTERMEASURE_COMBOTYPE_ID)
    self.theCountermeasureName = nameCtrl.GetValue()
    if (self.theCommitVerb == 'Create'):
      b = Borg()
      try:
        b.dbProxy.nameCheck(self.theCountermeasureName,'countermeasure')
      except ARM.ARMException,errorText:
        dlg = wx.MessageDialog(self,str(errorText),'Add countermeasure',wx.OK | wx.ICON_ERROR)
        dlg.ShowModal()
        dlg.Destroy()
        return

    self.theCountermeasureType = typeCtrl.GetValue()
    self.theCountermeasureDescription = descriptionCtrl.GetValue()
    try:
      self.theEnvironmentProperties = self.environmentPanel.environmentProperties()
    except ARM.EnvironmentValidationError, errorText:
      dlg = wx.MessageDialog(self,str(errorText),commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    
    commitLabel = self.theCommitVerb + ' countermeasure'

    if (len(self.theCountermeasureName) == 0):
      dlg = wx.MessageDialog(self,'No name entered',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theCountermeasureType) == 0):
      dlg = wx.MessageDialog(self,'No name selected',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theCountermeasureDescription) == 0):
      dlg = wx.MessageDialog(self,'No description entered',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    elif (len(self.theEnvironmentProperties) == 0):
      dlg = wx.MessageDialog(self,'No environment specific properties set',commitLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return -1
    else:
      return 0

  def parameters(self):
    return CountermeasureParameters(self.theCountermeasureName,self.theCountermeasureDescription,self.theCountermeasureType,self.theEnvironmentProperties)
