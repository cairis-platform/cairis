import wx

class BasePanel(wx.Panel):
  def init(self,parent,winId):
    wx.Panel.__init__(self,parent,winId)

  def buildTextSizer(self,labelTxt,widgetSize,winId,toolTip='',isReadOnly=False):
    tBox = wx.StaticBox(self,-1,labelTxt)
    textSizer = wx.StaticBoxSizer(tBox,wx.HORIZONTAL)
    textCtrl = 0
    if (isReadOnly):
      textCtrl = wx.TextCtrl(self,winId,"",style=wx.TE_READONLY)
    else:
      textCtrl = wx.TextCtrl(self,winId,"")

    if (toolTip != ''):
      textCtrl.SetToolTip(wx.ToolTip(toolTip))
    textSizer.Add(textCtrl,1,wx.EXPAND)
    return textSizer

  def buildComboSizerList(self,labelTxt,widgetSize,winId,objtList):
    cslBox = wx.StaticBox(self,-1,labelTxt)
    comboSizer = wx.StaticBoxSizer(cslBox,wx.HORIZONTAL)
    objtComboCtrl = wx.ComboBox(self,winId,"",choices=objtList,size=widgetSize,style=wx.CB_READONLY)
    comboSizer.Add(objtComboCtrl,1,wx.EXPAND)
    return comboSizer

  def buildCommitButtonSizer(self,winId,isCreate):
    buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
    commitLabel = ''
    if (isCreate):
      commitLabel = 'Create'
    else:
      commitLabel = 'Update'
    createButton = wx.Button(self,winId,commitLabel)
    buttonSizer.Add(createButton)
    cancelButton = wx.Button(self,wx.ID_CANCEL,"Close")
    buttonSizer.Add(cancelButton)
    return buttonSizer

  def buildAddDeleteCloseButtonSizer(self,addId,deleteId,orientation=wx.VERTICAL):
    buttonSizer = wx.BoxSizer(orientation)
    addButton = wx.Button(self,addId,"Add")
    buttonSizer.Add(addButton)
    deleteButton = wx.Button(self,deleteId,"Delete")
    buttonSizer.Add(deleteButton)
    closeButton = wx.Button(self,wx.ID_CLOSE,"Close")
    buttonSizer.Add(closeButton)
    return buttonSizer

  def buildTraceListCtrl(self,winId,columnNames,traces):
    listCtrl = wx.ListCtrl(self,winId,style=wx.LC_REPORT)
    for idx,columnName in enumerate(columnNames):
      listCtrl.InsertColumn(idx,columnName)

    b = Borg()
    dbProxy = b.dbProxy
    listRow  = 0
    for idx, objt in enumerate(traces):
      listCtrl.InsertStringItem(objt.fromObject())
      listCtrl.SetColumnWidth(0,75)
      listCtrl.SetStringItem(listRow,1,objt.fromName())
      listCtrl.SetColumnWidth(1,250)
      listCtrl.SetStringItem(objt.toObject())
      listCtrl.SetColumnWidth(2,75)
      listCtrl.SetStringItem(listRow,3,objt.toName())
      listCtrl.SetColumnWidth(3,125)
      listRow += 1
    return listCtrl

  def buildMLTextSizer(self,labelTxt,widgetSize,winId,isReadOnly=False):
    mltBox = wx.StaticBox(self,-1,labelTxt)
    textSizer = wx.StaticBoxSizer(mltBox,wx.HORIZONTAL)
    if (isReadOnly):
      textCtrl = wx.TextCtrl(self,winId,"",size=widgetSize,style=wx.TE_MULTILINE | wx.TE_READONLY)
    else:
      textCtrl = wx.TextCtrl(self,winId,"",size=widgetSize,style=wx.TE_MULTILINE)
    textSizer.Add(textCtrl,1,wx.EXPAND)
    return textSizer

  def buildCheckSizer(self,labelTxt,winId,isChecked):
    checkBox = wx.StaticBox(self,-1,labelTxt)
    checkSizer = wx.StaticBoxSizer(checkBox,wx.HORIZONTAL)
    ctrl = wx.CheckBox(self,winId,"")
    ctrl.SetValue(isChecked)
    checkSizer.Add(ctrl,1,wx.EXPAND)
    return checkSizer

