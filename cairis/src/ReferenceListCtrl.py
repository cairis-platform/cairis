#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ReferenceListCtrl.py $ $Id: ReferenceListCtrl.py 471 2011-05-15 17:34:25Z shaf $
import wx
import armid
import ARM
from Borg import Borg
from ReferenceDialog import ReferenceDialog
from ReferenceSynopsisDialog import ReferenceSynopsisDialog
from ReferenceContributionDialog import ReferenceContributionDialog

class ReferenceListCtrl(wx.ListCtrl):
  def __init__(self,parent,winId,crTypeName,pName = '',boxSize=wx.DefaultSize):
    wx.ListCtrl.__init__(self,parent,winId,size=boxSize,style=wx.LC_REPORT)
    self.thePersonaName = ''
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theCharacteristicType = crTypeName
    self.theReferenceTypeDictionary = {}
    self.InsertColumn(0,'Reference')
    self.SetColumnWidth(0,250)
    self.InsertColumn(1,'Description')
    self.SetColumnWidth(1,400)

    self.theSelectedIdx = -1
    self.theDimMenu = wx.Menu()
    self.theDimMenu.Append(armid.DIMLIST_MENUADD_ID,'Add')
    self.theDimMenu.Append(armid.DIMLIST_MENUDELETE_ID,'Delete')
    self.theDimMenu.Append(armid.CLC_MENU_REFERENCESYNOPSIS_ID,'Reference Synopsis')
    self.theDimMenu.Append(armid.CLC_MENU_REFERENCECONTRIBUTION_ID,'Reference Contribution')

    self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK,self.OnRightDown)
    wx.EVT_MENU(self.theDimMenu,armid.DIMLIST_MENUADD_ID,self.onAddReference)
    wx.EVT_MENU(self.theDimMenu,armid.DIMLIST_MENUDELETE_ID,self.onDeleteReference)
    wx.EVT_MENU(self.theDimMenu,armid.CLC_MENU_REFERENCESYNOPSIS_ID,self.onReferenceSynopsis)
    wx.EVT_MENU(self.theDimMenu,armid.CLC_MENU_REFERENCECONTRIBUTION_ID,self.onReferenceContribution)

    self.rcItem = self.theDimMenu.FindItemById(armid.CLC_MENU_REFERENCECONTRIBUTION_ID)
    self.rcItem.Enable(False)


    self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected)
    self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.OnItemDeselected)
    self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.onReferenceActivated)

  def OnRightDown(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    if (self.rcItem != None):
      refName = self.GetItemText(self.theSelectedIdx)
      hs = self.dbProxy.hasReferenceSynopsis(refName)
      if (hs == True):
        charNames = self.dbProxy.referenceCharacteristic(refName)
        for charName in charNames:
          hcs = self.dbProxy.hasCharacteristicSynopsis(charName)
          if (hcs == True):
            self.rcItem.Enable(True)
            break
          else:
            self.rcItem.Enable(False)
      else:
        self.rcItem.Enable(False)
    self.PopupMenu(self.theDimMenu)


  def onAddReference(self,evt):
    dlg = ReferenceDialog(self,self.theCharacteristicType)
    if (dlg.ShowModal() == armid.CHARACTERISTICREFERENCE_BUTTONCOMMIT_ID):
      self.theSelectedIdx = self.GetItemCount()
      refName = dlg.reference()
      dimName = dlg.dimension()
      refDesc = dlg.description()
      self.InsertStringItem(self.theSelectedIdx,refName)
      self.SetStringItem(self.theSelectedIdx,1,refDesc)
      self.theReferenceTypeDictionary[refName] = dimName

  def onDeleteReference(self,evt):
    if (self.theSelectedIdx == -1):
      errorText = 'No reference selected'
      errorLabel = 'Delete ' + self.theCharacteristicType + ' reference'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      refName = self.GetItemText(self.theSelectedIdx)
      self.DeleteItem(self.theSelectedIdx)
      del self.theReferenceTypeDictionary[refName]
  
  def OnItemSelected(self,evt):
    self.theSelectedIdx = evt.GetIndex()

  def OnItemDeselected(self,evt):
    self.theSelectedIdx = -1

  def onReferenceActivated(self,evt):
    self.theSelectedIdx = evt.GetIndex()
    refName = self.GetItemText(self.theSelectedIdx)
    dimName = self.theReferenceTypeDictionary[refName]
    descItem = self.GetItem(self.theSelectedIdx,1)
    desc = descItem.GetText()
     
    dlg = ReferenceDialog(self,self.theCharacteristicType,refName,desc,dimName)
    if (dlg.ShowModal() == armid.CHARACTERISTICREFERENCE_BUTTONCOMMIT_ID):
      refName = dlg.reference()
      dimName = dlg.dimension()
      refDesc = dlg.description()
      self.SetStringItem(self.theSelectedIdx,0,refName)
      self.SetStringItem(self.theSelectedIdx,1,refDesc)
      self.theReferenceTypeDictionary[refName] = dimName

  def load(self,refs):
    for ref,desc,dim in refs:
      idx = self.GetItemCount()
      self.InsertStringItem(idx,ref)
      self.SetStringItem(idx,1,desc)
      self.theReferenceTypeDictionary[ref] = dim

  def dimensions(self):
    refs = []
    for x in range(self.GetItemCount()):
      ref = self.GetItemText(x)
      dim = self.theReferenceTypeDictionary[ref]
      descItem = self.GetItem(x,1)
      desc = descItem.GetText()
      refs.append((ref,desc,dim))
    return refs

  def onReferenceSynopsis(self,evt):
    refName = self.GetItemText(self.theSelectedIdx)
    rs = self.dbProxy.getReferenceSynopsis(refName)
    dlg = ReferenceSynopsisDialog(self,rs)
    if (dlg.ShowModal() == armid.REFERENCESYNOPSIS_BUTTONCOMMIT_ID):
      if (rs.id() == -1):
        self.dbProxy.addReferenceSynopsis(dlg.parameters())
      else:
        self.dbProxy.updateReferenceSynopsis(dlg.parameters())

  def onReferenceContribution(self,evt):
    refName = self.GetItemText(self.theSelectedIdx)
    charNames = self.dbProxy.referenceCharacteristic(refName)
    for charName in charNames:
      rc = self.dbProxy.getReferenceContribution(charName,refName)
      dlg = ReferenceContributionDialog(self,rc)
      if (dlg.ShowModal() == armid.REFERENCECONTRIBUTION_BUTTONCOMMIT_ID):
        if (rc.meansEnd() == ''):
          self.dbProxy.addReferenceContribution(dlg.parameters())
        else:
          self.dbProxy.updateReferenceContribution(dlg.parameters())
