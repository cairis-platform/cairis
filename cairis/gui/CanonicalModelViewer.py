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


import gtk
import gtk.gdk
import kaosxdot
import NodeDialogFactory
import ModelMenuFactory
import os
from cairis.core.ARM import *
from cairis.core.Borg import *

class CanonicalModelViewer(kaosxdot.KaosDotWindow):
  def __init__(self,environmentName,modelType,locsName = ''):
    kaosxdot.KaosDotWindow.__init__(self,environmentName,modelType,locsName)
    b = Borg()
    self.dbProxy = b.dbProxy
    if environmentName != '':
      self.environment = self.dbProxy.dimensionObject(environmentName,'environment')
    else:
      self.environment = ''
    self.widget.connect('clicked', self.on_url_clicked)
    self.widget.connect('button_press_event', self.onClick)
    self.modelType = modelType

    directoryPrefix = b.imageDir + '/'

    if (modelType == 'class'):
      self.set_icon_from_file(directoryPrefix + 'classModel.png')
    elif (modelType == 'goal' or modelType == 'template_goal'):
      self.set_icon_from_file(directoryPrefix + 'goalModel.png')
    elif (modelType == 'obstacle'):
      self.set_icon_from_file(directoryPrefix + 'obstacleModel.png')
    elif (modelType == 'responsibility'):
      self.set_icon_from_file(directoryPrefix + 'responsibilityModel.png')
    elif (modelType == 'conceptmap'):
      self.set_icon_from_file(directoryPrefix + 'conceptMapModel.png')
    elif (modelType == 'location'):
      self.set_icon_from_file(directoryPrefix + 'location_view.png')

# Build some factory here based on the possible nodes we might have to click on
    if (modelType == 'goal' or modelType == 'obstacle'):
      menuOpts = ModelMenuFactory.build(self.modelType)
      self.menu = gtk.Menu()
      andItem = gtk.MenuItem(menuOpts[0])
      self.menu.append(andItem)
      orItem = gtk.MenuItem(menuOpts[1])
      self.menu.append(orItem)
      goalItem = gtk.MenuItem(menuOpts[2])
      self.menu.append(goalItem)
      subGoalItem = gtk.MenuItem(menuOpts[3])
      self.menu.append(subGoalItem)
      andReqItem = gtk.MenuItem(menuOpts[4])
      self.menu.append(andReqItem)
      subReqItem = gtk.MenuItem(menuOpts[5])
      self.menu.append(subReqItem)
      arItem = gtk.MenuItem(menuOpts[6])
      self.menu.append(arItem)
      andItem.connect("activate",self.onAnd)
      orItem.connect("activate",self.onOr)
      goalItem.connect("activate",self.onGoal)
      subGoalItem.connect("activate",self.onSubGoal)
      andReqItem.connect("activate",self.onAndRequirement)
      subReqItem.connect("activate",self.onSubRequirement)
      arItem.connect("activate",self.onAssignResponsibility)
    elif (modelType == 'class'):
      menuOpts = ModelMenuFactory.build(self.modelType)
      self.menu = gtk.Menu()
      assocItem = gtk.MenuItem(menuOpts[0])
      self.menu.append(assocItem)
      assocItem.connect("activate",self.onAssociate)


  def onClick(self,widget,event):
    if event.button == 3:
      self.url = self.widget.get_url(event.x,event.y).url
      self.menu.show_all()
      self.menu.popup(None,None,None,event.button,event.time)
    return 1
 
  def on_url_clicked(self, widget, url, event):
    self.url = url
    urlElements = url.split('#')
    if (urlElements[0] != 'link'):
      if self.environment != '':
        dialog = NodeDialogFactory.build(url,self.environment.name())
    return True

  def onTypeClicked(self, widget, event):
    pass

  def onNameClicked(self, widget, event):
    pass

  def ShowModal(self, associations):
    self.updateModel(associations)
    self.connect('destroy', gtk.main_quit)
    self.set_modal(True)
    gtk.main()

  def updateModel(self,associations):
    self.canonicalModel = associations
    try:
      xdotcode = self.canonicalModel.graph()
      environmentNames = self.dbProxy.getDimensionNames('environment')
      environmentNames.sort(key=str.lower)

      if (self.modelType == 'goal' or self.modelType == 'template_goal'):
        goalNames = ucNames = []
        if self.environment != '':
          goalNames = self.dbProxy.environmentGoals(self.environment.name())
          goalNames.sort(key=str.lower)
          ucNames = self.dbProxy.environmentUseCases(self.environment.name())
          ucNames.sort(key=str.lower)
        self.loadFilters(environmentNames,goalNames,ucNames)
      elif (self.modelType == 'obstacle'):
        obsNames = self.dbProxy.environmentObstacles(self.environment.name())
        obsNames.sort(key=str.lower)
        self.loadFilters(environmentNames,obsNames)
      elif (self.modelType == 'class'):
        asNames = []
        if self.environment != '':
          asNames = self.dbProxy.environmentAssets(self.environment.name())
        asNames.sort(key=str.lower)
        self.loadFilters(environmentNames,asNames)
      elif (self.modelType == 'conceptmap'):
        asNames = self.dbProxy.environmentRequirements(self.environment.name())
        asNames.sort(key=str.lower)
        self.loadFilters(environmentNames,asNames)
      elif (self.modelType == 'task'):
        taskNames = self.dbProxy.environmentTasks(self.environment.name())
        mcNames = self.dbProxy.getDimensionNames('misusecase')
        taskNames.sort(key=str.lower)
        self.loadFilters(environmentNames,taskNames,mcNames)
      elif (self.modelType == 'responsibility'):
        roleNames = self.dbProxy.getDimensionNames('role')
        roleNames.sort(key=str.lower)
        self.loadFilters(environmentNames,roleNames)
      else:
        self.loadFilters(environmentNames)
      self.set_xdotcode(xdotcode)
      self.blockHandlers()
      if self.environment != '':
        self.environmentCombo.set_active(environmentNames.index(self.environment.name()))
      self.unblockHandlers()
      self.widget.zoom_to_fit()
    except ARMException,errorText:
      if hasattr(errorText, 'value'):
        if isinstance(errorText.value, DatabaseProxyException):
          print(errorText.value.value)
      else:
          print str(errorText)
#      dlg = wx.MessageDialog(self,str(errorText),'IRIS',wx.OK | wx.ICON_ERROR)
#      dlg.ShowModal()
#      dlg.Destroy()
#      return


  def onAnd(self,widget):
    dim,objtName = self.url.split('#')
    dialog = NodeDialogFactory.build(self.url,self.environment.name(),True,objtName,'and')
    return True

  def onOr(self,widget):
    dim,objtName = self.url.split('#')
    dialog = NodeDialogFactory.build(self.url,self.environment.name(),True,objtName,'or')
    return True

  def onGoal(self,widget):
    dim,objtName = self.url.split('#')
    dialog = NodeDialogFactory.build(self.url,self.environment.name(),False,objtName,None,True)
    return True

  def onSubGoal(self,widget):
    dim,objtName = self.url.split('#')
    dialog = NodeDialogFactory.build(self.url,self.environment.name(),False,objtName,None,False)
    return True

  def onAssociate(self,widget):
    dim,objtName = self.url.split('#')
    dialog = NodeDialogFactory.build(self.url,self.environment.name(),False,objtName,'associate')
    return True

  def onAndRequirement(self,widget):
    dim,objtName = self.url.split('#')
    dialog = NodeDialogFactory.build(self.url,self.environment.name(),False,objtName,'andrequirement')
    return True

  def onSubRequirement(self,widget):
    dim,objtName = self.url.split('#')
    dialog = NodeDialogFactory.build(self.url,self.environment.name(),False,objtName,'subrequirement')
    return True

  def onAssignResponsibility(self,widget):
    dim,objtName = self.url.split('#')
    dialog = NodeDialogFactory.build(self.url,self.environment.name(),False,objtName,'assign')
    return True
