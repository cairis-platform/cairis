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

from cairis.core.Borg import Borg
import wx.lib.imagebrowser
import os
from cairis.core.armid import *

class CodeNetworkView(wx.lib.imagebrowser.ImageView):
  def __init__(self,parent,winId,fileName = 'codenetwork'):
    wx.lib.imagebrowser.ImageView.__init__(self,parent,winId)
    self.parent = parent
    b = Borg()
    self.theImageFile = b.tmpDir + '/' + fileName + '.png'

  def onRightDown(self,evt):
    self.PopupMenu(self.parent.theViewMenu)

  def reloadImage(self):
    if os.path.exists(self.theImageFile):
      self.SetValue(self.theImageFile)

