#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonalImageView.py $ $Id: PersonalImageView.py 249 2010-05-30 17:07:31Z shaf $
import wx.lib.imagebrowser
import armid

class PersonalImageView(wx.lib.imagebrowser.ImageView):
  def __init__(self,parent,winId):
    wx.lib.imagebrowser.ImageView.__init__(self,parent,winId)
    self.theLoadMenu = wx.Menu()
    self.theImageFile = ''
    self.theLoadMenu.Append(armid.PIV_MENULOAD_LOADIMAGE_ID,'Load Image')

    self.Bind(wx.EVT_RIGHT_DOWN,self.onRightDown)
    wx.EVT_MENU(self,armid.PIV_MENULOAD_LOADIMAGE_ID,self.onLoadImage)


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
