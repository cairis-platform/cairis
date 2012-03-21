#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/CountermeasureTaskPersonaDialog.py $ $Id: CountermeasureTaskPersonaDialog.py 379 2010-12-27 13:54:30Z shaf $
import wx
import armid
import WidgetFactory
import MySQLDatabaseProxy

class CountermeasureTaskPersonaDialog(wx.Dialog):
  def __init__(self,parent,taskName,personaName,duration,frequency,demands,goalSupport):
    wx.Dialog.__init__(self,parent,armid.TASKPERSONA_ID,'Add Task Persona',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,400))
    self.theDuration = ''
    self.theFrequency = ''
    self.theDemands = ''
    self.theGoalSupport = ''
    mainSizer = wx.BoxSizer(wx.VERTICAL)

    suPropertyValues = ['High Help','Medium Help','Low Help','None','Low Hindrance','Medium Hindrance','High Hindrance']
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Task',(87,30),armid.COUNTERMEASURETASKPERSONA_TEXTTASK_ID,isReadOnly = True),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildTextSizer(self,'Persona',(87,30),armid.COUNTERMEASURETASKPERSONA_TEXTPERSONA_ID,isReadOnly = True),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Duration',(87,30),armid.COUNTERMEASURETASKPERSONA_COMBODURATION_ID,suPropertyValues),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Frequency',(87,30),armid.COUNTERMEASURETASKPERSONA_COMBOFREQUENCY_ID,suPropertyValues),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Demands',(87,30),armid.COUNTERMEASURETASKPERSONA_COMBODEMANDS_ID,suPropertyValues),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Goal Conflict',(87,30),armid.COUNTERMEASURETASKPERSONA_COMBOGOALSUPPORT_ID,suPropertyValues),0,wx.EXPAND)
    mainSizer.Add(wx.StaticText(self,-1),1,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.COUNTERMEASURETASKPERSONA_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.COUNTERMEASURETASKPERSONA_BUTTONADD_ID,self.onAdd)
   
    taskCtrl = self.FindWindowById(armid.COUNTERMEASURETASKPERSONA_TEXTTASK_ID)
    taskCtrl.SetValue(taskName)
    personaCtrl = self.FindWindowById(armid.COUNTERMEASURETASKPERSONA_TEXTPERSONA_ID)
    personaCtrl.SetValue(personaName)
    durCtrl = self.FindWindowById(armid.COUNTERMEASURETASKPERSONA_COMBODURATION_ID)
    durCtrl.SetStringSelection(duration)
    freqCtrl = self.FindWindowById(armid.COUNTERMEASURETASKPERSONA_COMBOFREQUENCY_ID)
    freqCtrl.SetStringSelection(frequency)
    demCtrl = self.FindWindowById(armid.COUNTERMEASURETASKPERSONA_COMBODEMANDS_ID)
    demCtrl.SetStringSelection(demands)
    gsupCtrl = self.FindWindowById(armid.COUNTERMEASURETASKPERSONA_COMBOGOALSUPPORT_ID)
    gsupCtrl.SetStringSelection(goalSupport)

  def onAdd(self,evt):
    durCtrl = self.FindWindowById(armid.COUNTERMEASURETASKPERSONA_COMBODURATION_ID)
    freqCtrl = self.FindWindowById(armid.COUNTERMEASURETASKPERSONA_COMBOFREQUENCY_ID)
    demCtrl = self.FindWindowById(armid.COUNTERMEASURETASKPERSONA_COMBODEMANDS_ID)
    gsupCtrl = self.FindWindowById(armid.COUNTERMEASURETASKPERSONA_COMBOGOALSUPPORT_ID)
    self.theDuration = durCtrl.GetStringSelection()
    self.theFrequency = freqCtrl.GetStringSelection()
    self.theDemands = demCtrl.GetStringSelection()
    self.theGoalSupport = gsupCtrl.GetStringSelection()

    if (len(self.theDuration) == 0):
      dlg = wx.MessageDialog(self,'No duration selected','Add Task Persona',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theFrequency) == 0):
      dlg = wx.MessageDialog(self,'No frequency selected','Add Task Persona',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDemands) == 0):
      dlg = wx.MessageDialog(self,'No demands selected','Add Task Persona',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theGoalSupport) == 0):
      dlg = wx.MessageDialog(self,'No goal support selected','Add Task Persona',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    else:
      self.EndModal(armid.COUNTERMEASURETASKPERSONA_BUTTONADD_ID)

  def duration(self): return self.theDuration
  def frequency(self): return self.theFrequency
  def demands(self): return self.theDemands
  def goalsupport(self): return self.theGoalSupport
