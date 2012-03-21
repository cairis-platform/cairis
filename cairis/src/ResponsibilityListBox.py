#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ResponsibilityListBox.py $ $Id: ResponsibilityListBox.py 249 2010-05-30 17:07:31Z shaf $
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
