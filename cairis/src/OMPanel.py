#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RMPanel.py $ $Id: RMPanel.py 426 2011-02-26 16:09:37Z shaf $
import wx
import os
import armid
from EditorBase import EditorBase
from ObstaclesGrid import ObstaclesGrid
from datetime import datetime

NAME_POS = 0
DEFINITION_POS = 1
CATEGORY_POS = 2
ORIGINATOR_POS = 3

class OMPanel(EditorBase):
  def __init__(self,parent,id):
    self.objectDimension = 'obstacle'
    self.objectLabel = 'Obstacles'
    self.statusBar = parent.statusBar
    EditorBase.__init__(self,parent,id)
    self.grid = ObstaclesGrid(self,self.modCombo,self.envCombo)
    self.sizer.Add( self.grid,1,wx.EXPAND )
    self.resizeColumns()
    self.SetSizeHints(1150,400)
    self.SetSizer(self.sizer)
    self.Bind(wx.EVT_COMBOBOX, self.onObjectChange,id = armid.RMFRAME_TOOL_COMBOOBJECT)
    self.Bind(wx.EVT_COMBOBOX, self.onEnvironmentChange,id = armid.RMFRAME_TOOL_COMBOENVIRONMENT)

    
  def onObjectChange(self,evt):
    obsName = self.modCombo.GetValue()
    self.updateObjectSelection(obsName)
    self.refresh()


  def updateEnvironments(self):
    obsName = self.modCombo.GetValue()
    envs = self.dbProxy.obstacleEnvironments(obsName)
    self.envCombo.SetItems(envs)
    if (len(envs) > 0):
      self.envCombo.SetValue(envs[1])
    


  def resizeColumns(self):
    self.grid.SetColSize(NAME_POS,200)
    self.grid.SetColSize(DEFINITION_POS,450)
    self.grid.SetColSize(CATEGORY_POS,150)
    self.grid.SetColSize(ORIGINATOR_POS,150)
    self.grid.SetDefaultRowSize(35)


  def updateObjectSelection(self,selectedObs = ''):
    obsName = self.modCombo.GetValue()
    if (obsName != ''):
      self.updateEnvironments()
    else:
      self.envCombo.Clear()
      self.envCombo.SetItems([''])
      self.envCombo.SetValue('')

    self.modCombo.Clear()

    envName = self.envCombo.GetValue()
    if (selectedObs == ''):
      obsMods = self.dbProxy.getDimensionNames(self.objectDimension,envName)
    else:
      obsMods = self.dbProxy.getSubObstacleNames(obsName,envName)

    obsMods.sort()
    self.modCombo.SetItems(obsMods)
    if (selectedObs != ''):
      self.modCombo.SetStringSelection(selectedObs)
    self.refresh()

  def onEnvironmentChange(self,evt):
    obsName = self.modCombo.GetValue()
    envName = self.envCombo.GetValue()
    obsMods = self.dbProxy.getSubObstacleNames(obsName,envName)
    self.modCombo.SetItems(obsMods)
    self.refresh()

  def relabel(self):
    envName = self.envCombo.GetValue()
    self.dbProxy.relabelObstacles(envName)
    self.statusBar.SetStatusText(str(datetime.now())[:19] + ' : obstacles relabelled')

  def addObject(self):
    grid = self.FindWindowById(armid.ID_REQGRID)
    pos = grid.GetGridCursorRow()
    grid.InsertRows(pos)

