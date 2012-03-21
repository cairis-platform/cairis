#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RequirementsDocumentationPanel.py $ $Id: RequirementsDocumentationPanel.py 341 2010-11-14 23:27:22Z shaf $
import wx
import armid

class RequirementsDocumentationPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.REQDOCPANEL_ID)
    checkSizer = wx.BoxSizer(wx.VERTICAL)

    self.projectPurposeCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKPROJECTPURPOSE_ID,'Project Purpose')
    self.projectPurposeCheck.SetValue(True)
    checkSizer.Add(self.projectPurposeCheck,0,wx.EXPAND)

    self.environmentsCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKENVIRONMENTS_ID,'Environments')
    self.environmentsCheck.SetValue(True)
    checkSizer.Add(self.environmentsCheck,0,wx.EXPAND)

    self.stakeholdersCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKSTAKEHOLDERS_ID,'Personas')
    self.stakeholdersCheck.SetValue(True)
    checkSizer.Add(self.stakeholdersCheck,0,wx.EXPAND)

    self.mandatedConstraintsCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKMANDATEDCONSTRAINTS_ID,'Mandated Constraints')
    self.mandatedConstraintsCheck.SetValue(True)
    checkSizer.Add(self.mandatedConstraintsCheck,0,wx.EXPAND)

    self.namingConventionsCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKNAMINGCONVENTIONS_ID,'Naming Conventions')
    self.namingConventionsCheck.SetValue(True)
    checkSizer.Add(self.namingConventionsCheck,0,wx.EXPAND)

    self.projectScopeCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKPROJECTSCOPE_ID,'Project Scope')
    self.projectScopeCheck.SetValue(True)
    checkSizer.Add(self.projectScopeCheck,0,wx.EXPAND)

    self.assetsCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKASSETS_ID,'Assets')
    self.assetsCheck.SetValue(True)
    checkSizer.Add(self.assetsCheck,0,wx.EXPAND)

    self.tasksCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKTASKS_ID,'Tasks')
    self.tasksCheck.SetValue(True)
    checkSizer.Add(self.tasksCheck,0,wx.EXPAND)

    self.ucsCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKUSECASES_ID,'Use Cases')
    self.ucsCheck.SetValue(True)
    checkSizer.Add(self.ucsCheck,0,wx.EXPAND)

    self.goalsCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKGOALS_ID,'Goals')
    self.goalsCheck.SetValue(True)
    checkSizer.Add(self.goalsCheck,0,wx.EXPAND)

    self.responsibilityCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKRESPONSIBILITIES_ID,'Responsibilities')
    self.responsibilityCheck.SetValue(True)
    checkSizer.Add(self.responsibilityCheck,0,wx.EXPAND)

    self.requirementsCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKREQUIREMENTS_ID,'Requirements')
    self.requirementsCheck.SetValue(True)
    checkSizer.Add(self.requirementsCheck,0,wx.EXPAND)

    self.obstaclesCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKOBSTACLES_ID,'Obstacles')
    self.obstaclesCheck.SetValue(True)
    checkSizer.Add(self.obstaclesCheck,0,wx.EXPAND)

    self.vulnerabilitiesCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKVULNERABILITIES_ID,'Vulnerabilities')
    self.vulnerabilitiesCheck.SetValue(True)
    checkSizer.Add(self.vulnerabilitiesCheck,0,wx.EXPAND)

    self.attackersCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKATTACKERS_ID,'Attackers')
    self.attackersCheck.SetValue(True)
    checkSizer.Add(self.attackersCheck,0,wx.EXPAND)

    self.threatsCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKTHREATS_ID,'Threats')
    self.threatsCheck.SetValue(True)
    checkSizer.Add(self.threatsCheck,0,wx.EXPAND)

    self.risksCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKRISKS_ID,'Risks')
    self.risksCheck.SetValue(True)
    checkSizer.Add(self.risksCheck,0,wx.EXPAND)

    self.misuseCasesCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKMISUSECASES_ID,'Misuse Cases')
    self.misuseCasesCheck.SetValue(True)
    checkSizer.Add(self.misuseCasesCheck,0,wx.EXPAND)

    self.responsesCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKRESPONSES_ID,'Responses')
    self.responsesCheck.SetValue(True)
    checkSizer.Add(self.responsesCheck,0,wx.EXPAND)

    self.countermeasuresCheck = wx.CheckBox(self,armid.REQDOCPANEL_CHECKCOUNTERMEASURES_ID,'Countermeasures')
    self.countermeasuresCheck.SetValue(True)
    checkSizer.Add(self.countermeasuresCheck,0,wx.EXPAND)

    self.SetSizer(checkSizer)

  def sectionFlags(self):
    flags = [
      self.projectPurposeCheck.GetValue(),
      self.environmentsCheck.GetValue(),
      self.stakeholdersCheck.GetValue(),
      self.mandatedConstraintsCheck.GetValue(),
      self.namingConventionsCheck.GetValue(),
      self.projectScopeCheck.GetValue(),
      self.assetsCheck.GetValue(),
      self.tasksCheck.GetValue(),
      self.ucsCheck.GetValue(),
      self.goalsCheck.GetValue(),
      self.responsibilityCheck.GetValue(),
      self.requirementsCheck.GetValue(),
      self.obstaclesCheck.GetValue(),
      self.vulnerabilitiesCheck.GetValue(),
      self.attackersCheck.GetValue(),
      self.threatsCheck.GetValue(),
      self.risksCheck.GetValue(),
      self.misuseCasesCheck.GetValue(),
      self.responsesCheck.GetValue(),
      self.countermeasuresCheck.GetValue()
    ]
    return flags
