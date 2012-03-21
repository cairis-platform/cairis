#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TaskPersonaDialog.py $ $Id: TaskPersonaDialog.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import WidgetFactory

class TaskPersonaDialog(wx.Dialog):
  def __init__(self,parent,setPersonas,currentEnvironmentName,dp,pName='',pDur='',pFreq='',pDem='',pGsup=''):
    wx.Dialog.__init__(self,parent,armid.TASKPERSONA_ID,'Add Task Persona',style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX|wx.THICK_FRAME|wx.RESIZE_BORDER,size=(400,300))
    self.theName = pName
    self.theDuration = pDur
    self.theFrequency = pFreq
    self.theDemands = pDem
    self.theGoalSupport = pGsup
    mainSizer = wx.BoxSizer(wx.VERTICAL)
    personaList = dp.getDimensionNames('persona',currentEnvironmentName)

    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Name',(87,30),armid.TASKPERSONA_COMBONAME_ID,personaList),0,wx.EXPAND)
    suList = ['None','Low','Medium','High']
    durationList = ['Seconds','Minutes','Hours or longer']
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Duration',(87,30),armid.TASKPERSONA_COMBODURATION_ID,durationList),0,wx.EXPAND)
    freqList = ['Hourly or more','Daily - Weekly','Monthly or less']
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Frequency',(87,30),armid.TASKPERSONA_COMBOFREQUENCY_ID,freqList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Demands',(87,30),armid.TASKPERSONA_COMBODEMANDS_ID,suList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildComboSizerList(self,'Goal Conflict',(87,30),armid.TASKPERSONA_COMBOGOALSUPPORT_ID,suList),0,wx.EXPAND)
    mainSizer.Add(WidgetFactory.buildAddCancelButtonSizer(self,armid.TASKPERSONA_BUTTONADD_ID),0,wx.ALIGN_CENTER)
    if (self.theName != ''):
      self.SetLabel('Edit Task Persona')
      nameCtrl = self.FindWindowById(armid.TASKPERSONA_COMBONAME_ID)
      nameCtrl.SetValue(self.theName)
      durCtrl = self.FindWindowById(armid.TASKPERSONA_COMBODURATION_ID)
      durCtrl.SetStringSelection(self.theDuration)
      freqCtrl = self.FindWindowById(armid.TASKPERSONA_COMBOFREQUENCY_ID)
      freqCtrl.SetStringSelection(self.theFrequency)
      demCtrl = self.FindWindowById(armid.TASKPERSONA_COMBODEMANDS_ID)
      demCtrl.SetStringSelection(self.theDemands)
      gsupCtrl = self.FindWindowById(armid.TASKPERSONA_COMBOGOALSUPPORT_ID)
      gsupCtrl.SetStringSelection(self.theGoalSupport)
    self.SetSizer(mainSizer)

    wx.EVT_BUTTON(self,armid.TASKPERSONA_BUTTONADD_ID,self.onAdd)

  def onAdd(self,evt):
    nameCtrl = self.FindWindowById(armid.TASKPERSONA_COMBONAME_ID)
    durCtrl = self.FindWindowById(armid.TASKPERSONA_COMBODURATION_ID)
    freqCtrl = self.FindWindowById(armid.TASKPERSONA_COMBOFREQUENCY_ID)
    demCtrl = self.FindWindowById(armid.TASKPERSONA_COMBODEMANDS_ID)
    gsupCtrl = self.FindWindowById(armid.TASKPERSONA_COMBOGOALSUPPORT_ID)
    self.theName = nameCtrl.GetValue()
    self.theDuration = durCtrl.GetValue()
    self.theFrequency = freqCtrl.GetValue()
    self.theDemands = demCtrl.GetValue()
    self.theGoalSupport = gsupCtrl.GetValue()


    if len(self.theName) == 0:
      dlg = wx.MessageDialog(self,'No name selected','Add Task Persona',wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
      return
    elif (len(self.theDuration) == 0):
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
      self.EndModal(armid.TASKPERSONA_BUTTONADD_ID)

  def persona(self): return self.theName
  def duration(self): return self.theDuration
  def frequency(self): return self.theFrequency
  def demands(self): return self.theDemands
  def goalsupport(self): return self.theGoalSupport
