#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ProjectSettingsDialog.py $ $Id: ProjectSettingsDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from ProjectSettingsPanel import ProjectSettingsPanel

class ProjectSettingsDialog(wx.Dialog):
  def __init__(self,parent,settingsDictionary,dictionary,contributors,revisions):
    wx.Dialog.__init__(self,parent,armid.PROJECTSETTINGS_ID,'Project Settings',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME,size=(600,500))
    self.theId = -1
    self.panel = 0
    self.theProjectName = settingsDictionary['Project Name']
    self.theBackground = settingsDictionary['Project Background']
    self.theGoals = settingsDictionary['Project Goals']
    self.theScope = settingsDictionary['Project Scope']
    self.theRichPicture = settingsDictionary['Rich Picture']
    self.theDefinitions = dictionary
    self.theContributors = contributors
    self.theRevisions = revisions
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    self.panel = ProjectSettingsPanel(self,self.theProjectName,self.theBackground,self.theGoals,self.theScope,self.theDefinitions,self.theContributors,self.theRevisions,self.theRichPicture)
    mainSizer.Add(self.panel,1,wx.EXPAND)
    self.SetSizer(mainSizer)
    wx.EVT_BUTTON(self,armid.PROJECTSETTINGS_BUTTONCOMMIT_ID,self.onCommit)

  def onCommit(self,evt):
    self.theProjectName = self.panel.name()
    self.theBackground = self.panel.background()
    self.theGoals = self.panel.goals()
    self.theScope = self.panel.scope()
    self.theDefinitions = self.panel.definitions()
    self.theContributors = self.panel.contributors()
    self.theRevisions = self.panel.revisions()
    self.theRichPicture = self.panel.richPicture()
    self.EndModal(armid.PROJECTSETTINGS_BUTTONCOMMIT_ID)

  def name(self): return self.theProjectName
  def background(self): return self.theBackground
  def goals(self): return self.theGoals
  def scope(self): return self.theScope
  def definitions(self): return self.theDefinitions
  def contributors(self): return self.theContributors
  def revisions(self): return self.theRevisions
  def richPicture(self): return self.theRichPicture
