#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TaskPanel.py $ $Id: TaskPanel.py 581 2012-03-19 17:48:11Z shaf $
import wx
import armid
from BasePanel import BasePanel
from TaskEnvironmentPanel import TaskEnvironmentPanel
from TCNarrativeTextCtrl import TCNarrativeTextCtrl

class TaskPanel(BasePanel):
  def __init__(self,parent,dp):
    BasePanel.__init__(self,parent,armid.TASK_ID)
    self.dbProxy = dp
 
  def buildControls(self,isCreate,isUpdateable = True):
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    summBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
    mainSizer.Add(summBoxSizer,0,wx.EXPAND)
    summBoxSizer.Add(self.buildTextSizer('Name',(87,30),armid.TASK_TEXTNAME_ID),1,wx.EXPAND)
    summBoxSizer.Add(self.buildTextSizer('Code',(87,30),armid.TASK_TEXTSHORTCODE_ID),1,wx.EXPAND)
    mainSizer.Add(self.buildTextSizer('Author',(87,30),armid.TASK_TEXTAUTHOR_ID),0,wx.EXPAND)
    mainSizer.Add(self.buildCheckSizer('Assumption Task',armid.TASK_CHECKASSUMPTION_ID,False),0,wx.EXPAND)

    oBox = wx.StaticBox(self,-1,'Objective')
    oSizer = wx.StaticBoxSizer(oBox,wx.HORIZONTAL)
    oSizer.Add(TCNarrativeTextCtrl(self,armid.TASK_TEXTOBJECTIVE_ID),1,wx.EXPAND)
    mainSizer.Add(oSizer,0,wx.EXPAND)

    self.environmentPanel = TaskEnvironmentPanel(self,self.dbProxy)
    mainSizer.Add(self.environmentPanel,1,wx.EXPAND)
    mainSizer.Add(self.buildCommitButtonSizer(armid.TASK_BUTTONCOMMIT_ID,isCreate),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

  def loadControls(self,task,isReadOnly=False):
    nameCtrl = self.FindWindowById(armid.TASK_TEXTNAME_ID)
    nameCtrl.SetValue(task.name())
    shortCodeCtrl = self.FindWindowById(armid.TASK_TEXTSHORTCODE_ID)
    shortCodeCtrl.SetValue(task.shortCode())
    authorCtrl = self.FindWindowById(armid.TASK_TEXTAUTHOR_ID)
    authorCtrl.SetValue(task.author())
    assumptionCtrl = self.FindWindowById(armid.TASK_CHECKASSUMPTION_ID)
    assumptionCtrl.SetValue(task.assumption())
    objectiveCtrl = self.FindWindowById(armid.TASK_TEXTOBJECTIVE_ID)
    objectiveCtrl.Set(task.name(),task.objective())
    self.environmentPanel.loadControls(task)
