#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


import os
import pprint
import random
import wx
from cairis.core.armid import *
from cairis.core.Borg import Borg
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
  FigureCanvasWxAgg as FigCanvas, \
  NavigationToolbar2WxAgg as NavigationToolbar

__author__ = 'Shamal Faily'

def riskColourCode(riskScore):
  if (riskScore <= 1):
    return '#fef2ec'
  elif (riskScore == 2):
    return '#fcd9c8'
  elif (riskScore == 3):
    return '#f7ac91'
  elif (riskScore == 4):
    return '#f67e61'
  elif (riskScore == 5):
    return '#f2543d'
  elif (riskScore == 6):
    return '#e42626'
  elif (riskScore == 7):
    return '#b9051a'
  elif (riskScore == 8):
    return '#900014'
  else:
    return '#52000D'

class RiskScatterPanel(wx.Panel):
  def __init__(self,parent):
    wx.Panel.__init__(self,parent,RISKSCATTER_ID)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.dpi = 100
    self.fig = Figure((5.0, 4.0), dpi=self.dpi)
    self.canvas = FigCanvas(self, -1, self.fig)
    self.axes = self.fig.add_subplot(111,xlabel='Severity',ylabel='Likelihood',autoscale_on=False)
    self.axes.set_xticklabels(['Marginal','Critical','Catastrophic'])
    self.axes.set_yticks([0,1,2,3,4,5])
    self.toolbar = NavigationToolbar(self.canvas)

    envs = self.dbProxy.getDimensionNames('environment')
    self.envCombo = wx.ComboBox(self,RISKSCATTER_COMBOENVIRONMENT_ID,envs[0],choices=envs,size=(300,-1),style=wx.CB_DROPDOWN)
    self.envCombo.Bind(wx.EVT_COMBOBOX,self.onEnvironmentChange)
    
    self.vbox = wx.BoxSizer(wx.VERTICAL)
    self.vbox.Add(self.toolbar, 0, wx.EXPAND)
    self.vbox.Add(self.envCombo,0, wx.EXPAND)
    self.vbox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
    self.SetSizer(self.vbox)
    self.vbox.Fit(self)
    self.drawScatter(envs[0])
    
  def drawScatter(self,envName):
    self.axes.clear()        
    self.axes.grid(True)
    self.axes.set_xlabel('Severity')
    self.axes.set_ylabel('Likelihood')
    self.axes.set_xbound(0,4)
    self.axes.set_ybound(0,5)
    xs,ys,cs = self.dbProxy.riskScatter(envName)
    ccs = []
    for c in cs:
      ccs.append(riskColourCode(c))

    if ((len(xs) > 0) and (len(ys) > 0)):
      self.axes.scatter(xs,ys,c=ccs,marker='d')
    self.canvas.draw()

  def onEnvironmentChange(self,evt):
    envName = self.envCombo.GetStringSelection()
    self.drawScatter(envName)
    
  def on_save_plot(self, event):
    fileChoices = "PNG (*.png)|*.png"
    dlg = wx.FileDialog(self,message="Save risk scatter",defaultDir=os.getcwd(),defaultFile="scatter.png",wildcard=fileChoices,style=wx.SAVE)
    if dlg.ShowModal() == wx.ID_OK:
      path = dlg.GetPath()
      self.canvas.print_figure(path, dpi=self.dpi)
