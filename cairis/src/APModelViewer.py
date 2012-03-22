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
import apxdot
import AssumptionNodeDialogFactory
import os
from ARM import *
from Borg import Borg

class APModelViewer(apxdot.APDotWindow):
  def __init__(self,pName = '',bvName = ''):
    apxdot.APDotWindow.__init__(self)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theInitialPersona = pName
    self.theInitialBv = bvName
    self.widget.connect('clicked', self.on_url_clicked)

    directoryPrefix = ''
    if (os.name == 'nt'):
      directoryPrefix += 'C:\\iris\\'
    elif (os.uname()[0] == 'Linux'):
      directoryPrefix += os.environ['IRIS_IMAGES'] + '/'
    elif (os.uname()[0] == 'Darwin'):
      directoryPrefix += os.environ['IRIS_IMAGES'] + '/'
    else:
      raise UnsupportedOperatingSystem(os.name)

    self.set_icon_from_file(directoryPrefix + 'apModel.png')


  def on_url_clicked(self, widget, url, event):
    self.url = url
    urlElements = url.split('#')
    if (urlElements[0] != 'link'):
      dialog = AssumptionNodeDialogFactory.build(url)
    return True

  def ShowModal(self, associations):
    self.updateModel(associations)
    self.connect('destroy', gtk.main_quit)
    self.set_modal(True)
    gtk.main()

  def updateModel(self,associations):
    self.canonicalModel = associations
    try:
      xdotcode = self.canonicalModel.graph()

      personaNames = self.dbProxy.getDimensionNames('persona')
      bvNames = self.dbProxy.getDimensionNames('behavioural_variable')
      charNames = self.canonicalModel.personaCharacteristics

      self.loadFilters(personaNames,bvNames,charNames)
      self.set_xdotcode(xdotcode)
      self.widget.zoom_to_fit()
    except ARMException,errorText:
      print str(errorText)
#      dlg = wx.MessageDialog(self,str(errorText),'IRIS',wx.OK | wx.ICON_ERROR)
#      dlg.ShowModal()
#      dlg.Destroy()
#      return
