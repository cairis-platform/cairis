#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonasDocumentationPanel.py $ $Id: PersonasDocumentationPanel.py 329 2010-10-31 14:59:16Z shaf $
import wx
import armid

class PersonasDocumentationPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.PERDOCPANEL_ID)
    checkSizer = wx.BoxSizer(wx.VERTICAL)

    self.projectPurposeCheck = wx.CheckBox(self,armid.PERDOCPANEL_CHECKPROJECTPURPOSE_ID,'Project Purpose')
    self.projectPurposeCheck.SetValue(True)
    checkSizer.Add(self.projectPurposeCheck,0,wx.EXPAND)

    self.projectScopeCheck = wx.CheckBox(self,armid.PERDOCPANEL_CHECKPROJECTSCOPE_ID,'Project Scope')
    self.projectScopeCheck.SetValue(True)
    checkSizer.Add(self.projectScopeCheck,0,wx.EXPAND)

    self.environmentsCheck = wx.CheckBox(self,armid.PERDOCPANEL_CHECKENVIRONMENTS_ID,'Environments')
    self.environmentsCheck.SetValue(True)
    checkSizer.Add(self.environmentsCheck,0,wx.EXPAND)

    self.stakeholdersCheck = wx.CheckBox(self,armid.PERDOCPANEL_CHECKSTAKEHOLDERS_ID,'Personas')
    self.stakeholdersCheck.SetValue(True)
    checkSizer.Add(self.stakeholdersCheck,0,wx.EXPAND)

    self.tasksCheck = wx.CheckBox(self,armid.PERDOCPANEL_CHECKTASKS_ID,'Tasks')
    self.tasksCheck.SetValue(True)
    checkSizer.Add(self.tasksCheck,0,wx.EXPAND)

    self.SetSizer(checkSizer)

  def sectionFlags(self):
    flags = [
      self.projectPurposeCheck.GetValue(),
      self.projectScopeCheck.GetValue(),
      self.environmentsCheck.GetValue(),
      self.stakeholdersCheck.GetValue(),
      self.tasksCheck.GetValue()
    ]
    return flags
