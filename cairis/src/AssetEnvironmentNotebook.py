#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssetEnvironmentNotebook.py $ $Id: AssetEnvironmentNotebook.py 436 2011-03-13 11:46:43Z shaf $
import wx
import armid
from ValueDictionary import ValueDictionary
from PropertiesListCtrl import PropertiesListCtrl
from AssetAssociationListCtrl import AssetAssociationListCtrl

class PropertiesPage(wx.Panel):
  def __init__(self,parent,dp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)
    pBox = wx.StaticBox(self,-1)
    pBoxSizer = wx.StaticBoxSizer(pBox,wx.HORIZONTAL)
    topSizer.Add(pBoxSizer,1,wx.EXPAND)
    values = ['None','Low','Medium','High']
    valueLookup = ValueDictionary(values)
    self.propertiesList = PropertiesListCtrl(self,armid.ASSETENVIRONMENT_LISTPROPERTIES_ID,valueLookup)
    pBoxSizer.Add(self.propertiesList,1,wx.EXPAND)

    self.SetSizer(topSizer)

class AssociationsPage(wx.Panel):
  def __init__(self,parent,winId,dp,pp):
    wx.Panel.__init__(self,parent)
    topSizer = wx.BoxSizer(wx.VERTICAL)

    asBox = wx.StaticBox(self,-1)
    asBoxSizer = wx.StaticBoxSizer(asBox,wx.HORIZONTAL)
    topSizer.Add(asBoxSizer,1,wx.EXPAND)
    self.associationList = AssetAssociationListCtrl(self,winId,dp,pp.propertiesList)
    asBoxSizer.Add(self.associationList,1,wx.EXPAND)
    self.SetSizer(topSizer)


class AssetEnvironmentNotebook(wx.Notebook):
  def __init__(self,parent,dp):
    wx.Notebook.__init__(self,parent,armid.ASSET_NOTEBOOKENVIRONMENT_ID)
    p1 = PropertiesPage(self,dp)
    p2 = AssociationsPage(self,armid.ASSET_LISTASSOCIATIONS_ID,dp,p1)
    self.AddPage(p1,'Properties')
    self.AddPage(p2,'Associations')
