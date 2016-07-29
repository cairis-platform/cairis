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


import wx.lib.imagebrowser
from cairis.core.armid import *

__author__ = 'Shamal Faily'

class PersonalImageView(wx.lib.imagebrowser.ImageView):
  def __init__(self,parent,winId):
    wx.lib.imagebrowser.ImageView.__init__(self,parent,winId)
    self.theLoadMenu = wx.Menu()
    self.theImageFile = ''
    self.theLoadMenu.Append(PIV_MENULOAD_LOADIMAGE_ID,'Load Image')

    self.Bind(wx.EVT_RIGHT_DOWN,self.onRightDown)
    wx.EVT_MENU(self,PIV_MENULOAD_LOADIMAGE_ID,self.onLoadImage)


  def onRightDown(self,evt):
    self.PopupMenu(self.theLoadMenu)

  def onLoadImage(self,evt):
    dlg = wx.FileDialog(None,style = wx.OPEN)
    if (dlg.ShowModal() == wx.ID_OK):
      self.theImageFile = dlg.GetPath()
      self.SetValue(self.theImageFile)
    dlg.Destroy()

  def loadImage(self,imageFile):
    if (imageFile != ''):
      self.theImageFile = imageFile
      self.SetValue(self.theImageFile)

  def personaImage(self):
    return self.theImageFile
