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
import componentxdot
import NodeDialogFactory
import ModelMenuFactory
import os
from ARM import *
from Borg import Borg

class ComponentModelViewer(componentxdot.ComponentDotWindow):
  def __init__(self,cvName):
    componentxdot.ComponentDotWindow.__init__(self,'',cvName)
    self.widget.connect('clicked', self.on_url_clicked)
    self.widget.connect('button_press_event', self.onClick)
    b = Borg()
    directoryPrefix = b.imageDir + '/'
    self.set_icon_from_file(directoryPrefix + 'component_view.png')

  def onClick(self,widget,event):
    if event.button == 3:
      self.url = self.widget.get_url(event.x,event.y).url
      self.menu.show_all()
      self.menu.popup(None,None,None,event.button,event.time)
    return 1
 
  def on_url_clicked(self, widget, url, event):
    self.url = url
    urlElements = url.split('#')
    if (urlElements[0] != 'connector'):
      dialog = NodeDialogFactory.buildComponentModelNode(url)
    return True

  def ShowModal(self, associations):
    self.updateModel(associations)
    self.connect('destroy', gtk.main_quit)
    self.set_modal(False)
    gtk.main()

  def updateModel(self,associations):
    self.canonicalModel = associations
    try:
      xdotcode = self.canonicalModel.graph()
      self.set_xdotcode(xdotcode)
      self.widget.zoom_to_fit()
    except ARMException,errorText:
      print str(errorText)
#      dlg = wx.MessageDialog(self,str(errorText),'IRIS',wx.OK | wx.ICON_ERROR)
#      dlg.ShowModal()
#      dlg.Destroy()
#      return
