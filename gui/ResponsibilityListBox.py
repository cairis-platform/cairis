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


import wx
import armid
import ARM
from DimensionListBox import DimensionListBox

class ResponsibilityListBox(DimensionListBox):
  def __init__(self,parent,winId,boxSize,dp):
    DimensionListBox.__init__(self,parent,winId,boxSize,'responsibility',dp)

  def onDeleteDimension(self,evt):
    idx = self.GetSelection()
    if (idx == -1):
      errorText = 'No ' + self.theDimensionTable + ' selected'
      errorLabel = 'Delete responsibility'
      dlg = wx.MessageDialog(self,errorText,errorLabel,wx.OK)
      dlg.ShowModal()
      dlg.Destroy()
    else:
      self.theSelectedValue = self.GetStringSelection()
      roles = self.dbProxy.responsibleRoles(self.theSelectedValue)
      if (len(roles) == 0):
        self.Delete(self.theSelectedValue)
      else:
        roleNames = ''
        if (len(roles) == 1): roleNames = roles[0]
        else:
          for idx,role in enumerate(roles):
            roleNames += role
            if (idx != (len(roles) - 1)):
              roleNames += ','
        errorMsg = 'Cannot delete responsibility due to dependent roles: ' + roleNames
        dlg = wx.MessageDialog(self,errorMsg,'Delete responsibility',wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
