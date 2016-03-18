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
from envxdot import EnvironmentDotWindow
from ARM import *
import NodeDialogFactory

class EnvironmentModelViewer(EnvironmentDotWindow):
  def __init__(self,environmentName,dp):
    EnvironmentDotWindow.__init__(self,environmentName,dp)
    self.dbProxy = dp
    self.environment = self.dbProxy.dimensionObject(environmentName,'environment')
    self.widget.connect('clicked', self.on_url_clicked)
    self.widget.connect('button_press_event', self.onClick)

  def onClick(self,widget,event):
    try:
      if event.button == 3:
        print self.widget.get_url(event.x,event.y).url
      return 1
    except AttributeError:
      pass
 
  def on_url_clicked(self, widget, url, event):
    dialog = NodeDialogFactory.build(url,self.environment.name())
    return True

  def onTypeClicked(self, widget, event):
    pass

  def onNameClicked(self, widget, event):
    pass

  def ShowModal(self, tLinks):
    self.updateModel(tLinks)
    self.connect('destroy', gtk.main_quit)
    self.set_modal(True)
    gtk.main()

  def updateModel(self,tLinks):
    self.traceModel = tLinks
    xdotcode = self.traceModel.graph()
    environmentNames = self.dbProxy.getDimensionNames('environment')
    environmentNames.sort(key=str.lower)
    self.loadFilters(environmentNames,tLinks.dimensions(),tLinks.objects())
    self.set_xdotcode(xdotcode)
    self.blockHandlers()
    self.environmentCombo.set_active(environmentNames.index(self.environment.name()))
    self.unblockHandlers()
    self.widget.zoom_to_fit()
