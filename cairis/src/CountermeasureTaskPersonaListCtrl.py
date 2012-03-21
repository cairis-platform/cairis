#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/CountermeasureTaskPersonaListCtrl.py $ $Id: CountermeasureTaskPersonaListCtrl.py 249 2010-05-30 17:07:31Z shaf $
import wx
import armid
import ARM
from CountermeasureTaskPersonaDialog import CountermeasureTaskPersonaDialog

class CountermeasureTaskPersonaListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,dp,boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.dbProxy = dp
    self.theCurrentEnvironment = ''
    self.theCurrentRole = ''
    self.InsertColumn(0,'Task')
    self.SetColumnWidth(0,150)
    self.InsertColumn(1,'Persona')
    self.SetColumnWidth(1,150)
    self.InsertColumn(2,'Duration')
    self.SetColumnWidth(2,100)
    self.InsertColumn(3,'Frequency')
    self.SetColumnWidth(3,100)
    self.InsertColumn(4,'Demands')
    self.SetColumnWidth(4,100)
    self.InsertColumn(5,'Goals')
    self.SetColumnWidth(5,100)
    self.theSelectedIdx = -1
    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onPersonaActivated)

  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onPersonaActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    task = self.GetItemText(self.theSelectedIdx)
    persona = self.GetItem(self.theSelectedIdx,1)
    pDur = self.GetItem(self.theSelectedIdx,2)
    pFreq = self.GetItem(self.theSelectedIdx,3)
    pDem = self.GetItem(self.theSelectedIdx,4)
    pGsup = self.GetItem(self.theSelectedIdx,5)
     
    dlg = CountermeasureTaskPersonaDialog(self,task,persona.GetText(),pDur.GetText(),pFreq.GetText(),pDem.GetText(),pGsup.GetText())
    if (dlg.ShowModal() == armid.COUNTERMEASURETASKPERSONA_BUTTONADD_ID):
      self.SetStringItem(self.theSelectedIdx,2,dlg.duration())
      self.SetStringItem(self.theSelectedIdx,3,dlg.frequency())
      self.SetStringItem(self.theSelectedIdx,4,dlg.demands())
      self.SetStringItem(self.theSelectedIdx,5,dlg.goalsupport())

  def load(self,personas):
    for task,persona,dur,freq,dem,gsup in personas:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,task)
      self.SetStringItem(idx,1,persona)
      self.SetStringItem(idx,2,dur)
      self.SetStringItem(idx,3,freq)
      self.SetStringItem(idx,4,dem)
      self.SetStringItem(idx,5,gsup)

  def dimensions(self):
    personas = []
    for x in range(self.GetItemCount()):
      task = self.GetItemText(x)
      persona = self.GetItem(x,1)
      pDur = self.GetItem(x,2)
      pFreq = self.GetItem(x,3)
      pDem = self.GetItem(x,4)
      pGsup = self.GetItem(x,5)
      personas.append((task,persona.GetText(),pDur.GetText(),pFreq.GetText(),pDem.GetText(),pGsup.GetText()))
    return personas
