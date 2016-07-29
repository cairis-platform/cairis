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


import wx.combo
import os

__author__ = 'Shamal Faily'

class AssociationComboBox(wx.combo.OwnerDrawnComboBox):

  def OnDrawItem(self,dc,rect,item,flags):
    if item == wx.NOT_FOUND:
      return

    b = Borg()

    r = wx.Rect(*rect)
    r.Deflate(20,20)
    if (item == 0):
      if not hasattr(b, 'imageDir'):
        raise RuntimeError('imageDir was not defined by settings')
      png = wx.Image(os.path.join(b.imageDir, 'compositionAdornment.png'),wx.BITMAP_TYPE_PNG).ConvertToBitmap()
      dc.DrawBitmap(png,r.x,r.y)
    elif (item == 1):
      if not hasattr(b, 'imageDir'):
        raise RuntimeError('imageDir was not defined by settings')
      png = wx.Image(os.path.join(b.imageDir, 'aggregationAdornment.png'),wx.BITMAP_TYPE_PNG).ConvertToBitmap()
      dc.DrawBitmap(png,r.x,r.y)
    elif (item == 2):
      if not hasattr(b, 'imageDir'):
        raise RuntimeError('imageDir was not defined by settings')
      png = wx.Image(os.path.join(b.imageDir, 'associationAdornment.png'),wx.BITMAP_TYPE_PNG).ConvertToBitmap()
      dc.DrawBitmap(png,r.x,r.y)
