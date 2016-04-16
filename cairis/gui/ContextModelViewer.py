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
import contextxdot
import ContextNodeDialogFactory
import os
from cairis.core.Borg import *

class ContextModelViewer(contextxdot.ContextDotWindow):
  def __init__(self,environmentName,dp):
    contextxdot.ContextDotWindow.__init__(self,environmentName,dp)
    self.dbProxy = dp
    if (environmentName != ''):
      self.environment = self.dbProxy.dimensionObject(environmentName,'environment')
    else:
      self.environment = None
    self.widget.connect('clicked', self.on_url_clicked)
    self.widget.connect('button_press_event', self.onClick)
    self.set_icon_from_file(b.imageDir + '/contextModel.png')

  def onClick(self,widget,event):
    if event.button == 3:
      print 'right clicked ', self.widget.get_url(event.x,event.y).url
    return 1
 
  def on_url_clicked(self, widget, url, event):
    urlElements = url.split('#')
    if (urlElements[0] != 'link'):
      dialog = ContextNodeDialogFactory.build(url)
    return True

  def onTypeClicked(self, widget, event):
    pass

  def onNameClicked(self, widget, event):
    pass

  def ShowModal(self, associations):
    self.updateModel(associations)
    self.connect('destroy', gtk.main_quit)
    gtk.main()

  def updateModel(self,associations):
    self.canonicalModel = associations
    xdotcode = self.canonicalModel.graph()
    self.set_xdotcode(xdotcode)
    self.widget.zoom_to_fit()

  def updateModel(self,associations):
    self.canonicalModel = associations
    xdotcode = self.canonicalModel.graph()
    environmentNames = [''] + self.dbProxy.getDimensionNames('environment')
    environmentNames.sort(key=str.lower)
    self.loadFilters(environmentNames)
    self.set_xdotcode(xdotcode)
    self.blockHandlers()
    if (self.environment != None):
      self.environmentCombo.set_active(environmentNames.index(self.environment.name()))
    self.unblockHandlers()
    self.widget.zoom_to_fit()

