#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ThreatListBox.py $ $Id: ThreatListBox.py 523 2011-11-04 18:07:01Z shaf $
import wx
import DimensionListBox

class ThreatListBox(DimensionListBox.DimensionListBox):
  def __init__(self,parent,winId,boxSize,dimensionTable,dp):
    DimensionListBox.DimensionListBox.__init__(self,parent,winId,boxSize,dimensionTable,dp)
    self.theMCPanel = parent

  def onAddDimension(self,evt):
    DimensionListBox.DimensionListBox.onAddDimension(self,evt)    
    self.theMCPanel.addThreatAttacker(self.theSelectedValue)

  def onDeleteDimension(self,evt):
    DimensionListBox.DimensionListBox.onDeleteDimension(self,evt)    
    self.theMCPanel.deleteThreatAttacker(self.theSelectedValue)
