#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RMPanel.py $ $Id: RMPanel.py 564 2012-03-12 17:53:00Z shaf $
import wx
import os
import armid
from EditorBase import EditorBase
from RequirementsGrid import RequirementsGrid

NAME_POS = 0
DESCRIPTION_POS = 1
PRIORITY_POS = 2
RATIONALE_POS = 3
FITCRITERION_POS = 4
ORIGINATOR_POS = 5
TYPE_POS = 6

class RMPanel(EditorBase):
  def __init__(self,parent,id):
    self.objectDimension = 'asset'
    self.objectLabel = 'Assets'
    EditorBase.__init__(self,parent,id)
    self.grid = RequirementsGrid(self,self.modCombo,self.envCombo)
    self.sizer.Add( self.grid,1,wx.EXPAND )
    self.resizeColumns()
    self.SetSizeHints(1225,400)
    self.SetSizer(self.sizer)
    self.Bind(wx.EVT_COMBOBOX, self.onObjectChange,id = armid.RMFRAME_TOOL_COMBOOBJECT)
    self.Bind(wx.EVT_COMBOBOX, self.onEnvironmentChange,id = armid.RMFRAME_TOOL_COMBOENVIRONMENT)

  def onObjectChange(self,evt):
    self.envCombo.SetValue('')
    self.refresh()

  def onEnvironmentChange(self,evt):
    self.modCombo.SetValue('')
    self.refresh()


  def resizeColumns(self):
    self.grid.SetColSize(NAME_POS,150)
    self.grid.SetColSize(DESCRIPTION_POS,250)
    self.grid.SetColSize(PRIORITY_POS,65)
    self.grid.SetColSize(RATIONALE_POS,150)
    self.grid.SetColSize(FITCRITERION_POS,250)
    self.grid.SetColSize(ORIGINATOR_POS,100)
    self.grid.SetColSize(TYPE_POS,115)
    self.grid.SetDefaultRowSize(35)

  def relabel(self):
    pass

  def addObject(self):
    grid = self.FindWindowById(armid.ID_REQGRID)
    pos = grid.GetGridCursorRow()
    grid.InsertRows(pos)

