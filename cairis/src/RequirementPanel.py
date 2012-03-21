#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RequirementPanel.py $ $Id: RequirementPanel.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory

class RequirementPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,armid.REQUIREMENT_ID)

  def buildControls(self,isCreate,isUpdateable=True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Label',(87,30),armid.REQUIREMENT_TEXTLABEL_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Description',(87,60),armid.REQUIREMENT_TEXTDESCRIPTION_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Priority',(87,30),armid.REQUIREMENT_TEXTPRIORITY_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Rationale',(87,30),armid.REQUIREMENT_TEXTRATIONALE_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildMLTextSizer(self,'Fit Criterion',(87,60),armid.REQUIREMENT_TEXTFITCRITERION_ID),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Originator',(87,30),armid.REQUIREMENT_TEXTORIGINATOR_ID),0,wx.EXPAND)
    self.SetSizer(mainSizer)

  def loadControls(self,requirement,isReadOnly=False):
    labelCtrl = self.FindWindowById(armid.REQUIREMENT_TEXTLABEL_ID)
    descriptionCtrl = self.FindWindowById(armid.REQUIREMENT_TEXTDESCRIPTION_ID)
    priorityCtrl = self.FindWindowById(armid.REQUIREMENT_TEXTPRIORITY_ID)
    rationaleCtrl = self.FindWindowById(armid.REQUIREMENT_TEXTRATIONALE_ID)
    fitCriterionCtrl = self.FindWindowById(armid.REQUIREMENT_TEXTFITCRITERION_ID)
    originatorCtrl = self.FindWindowById(armid.REQUIREMENT_TEXTORIGINATOR_ID)
    labelCtrl.SetValue(requirement.label())
    descriptionCtrl.SetValue(requirement.description())
    priorityCtrl.SetValue(str(requirement.priority()))
    rationaleCtrl.SetValue(requirement.rationale())
    fitCriterionCtrl.SetValue(requirement.fitCriterion())
    originatorCtrl.SetValue(requirement.originator())
    if (isReadOnly):
      labelCtrl.Disable()
      descriptionCtrl.Disable()
      priorityCtrl.Disable()
      rationaleCtrl.Disable()
      fitCriterionCtrl.Disable()
      originatorCtrl.Disable()
