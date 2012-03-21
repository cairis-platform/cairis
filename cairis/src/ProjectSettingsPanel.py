#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ProjectSettingsPanel.py $ $Id: ProjectSettingsPanel.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
from ProjectSettingsNotebook import ProjectSettingsNotebook

class ProjectSettingsPanel(wx.Panel):
  def __init__(self,parent,projName,background,goals,scope,definitions,contributors,revisions,richPicture):
    wx.Panel.__init__(self,parent,armid.PROJECTSETTINGS_PANELSETTINGS_ID)
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    nbBox = wx.StaticBox(self,-1)
    nbSizer = wx.StaticBoxSizer(nbBox,wx.HORIZONTAL)
    mainSizer.Add(nbSizer,1,wx.EXPAND)
    self.notebook = ProjectSettingsNotebook(self)
    nbSizer.Add(self.notebook,1,wx.EXPAND)

    self.nameCtrl = self.notebook.FindWindowById(armid.PROJECTSETTINGS_TEXTPROJECTNAME_ID)
    self.nameCtrl.SetValue(projName)
    self.backgroundCtrl = self.notebook.FindWindowById(armid.PROJECTSETTINGS_TEXTBACKGROUND_ID)
    self.backgroundCtrl.SetValue(background)
    self.goalsCtrl = self.notebook.FindWindowById(armid.PROJECTSETTINGS_TEXTGOALS_ID)
    self.goalsCtrl.SetValue(goals)
    self.scopeCtrl = self.notebook.FindWindowById(armid.PROJECTSETTINGS_TEXTSCOPE_ID)
    self.scopeCtrl.SetValue(scope)
    self.definitionCtrl = self.notebook.FindWindowById(armid.PROJECTSETTINGS_LISTDICTIONARY_ID)
    self.definitionCtrl.load(definitions)
    self.contributorsCtrl = self.notebook.FindWindowById(armid.PROJECTSETTINGS_LISTCONTRIBUTORS_ID)
    self.contributorsCtrl.load(contributors)
    self.revisionsCtrl = self.notebook.FindWindowById(armid.PROJECTSETTINGS_LISTREVISIONS_ID)
    self.revisionsCtrl.load(revisions)
    self.richPictureCtrl = self.notebook.FindWindowById(armid.PROJECTSETTINGS_IMAGERICHPICTURE_ID)
    self.richPictureCtrl.loadImage(richPicture)

    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(buttonSizer,0,wx.ALIGN_CENTER)

    buttonSizer.Add(wx.Button(self,armid.PROJECTSETTINGS_BUTTONCOMMIT_ID,'Update'))
    buttonSizer.Add(wx.Button(self,wx.ID_CANCEL,'Cancel'))

    self.SetSizer(mainSizer)

  def name(self): return self.nameCtrl.GetValue()
  def background(self): return self.backgroundCtrl.GetValue()
  def goals(self): return self.goalsCtrl.GetValue()
  def scope(self): return self.scopeCtrl.GetValue()
  def definitions(self): return self.definitionCtrl.dimensions()
  def contributors(self): return self.contributorsCtrl.dimensions()
  def revisions(self): return self.revisionsCtrl.dimensions()
  def richPicture(self): return self.richPictureCtrl.personaImage()
