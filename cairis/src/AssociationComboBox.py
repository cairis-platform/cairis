#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssociationComboBox.py $ $Id: AssociationComboBox.py 330 2010-10-31 15:01:28Z shaf $
import wx.combo
import os

class AssociationComboBox(wx.combo.OwnerDrawnComboBox):

  def OnDrawItem(self,dc,rect,item,flags):
    directoryPrefix = ''
    if (os.name == 'nt'):
      directoryPrefix += 'C:\\iris\\'
    elif (os.uname()[0] == 'Linux'):
      directoryPrefix += os.environ['IRIS_IMAGES'] + '/'
    elif (os.uname()[0] == 'Darwin'):
      directoryPrefix += os.environ['IRIS_IMAGES'] + '/'
    else:
      raise UnsupportedOperatingSystem(os.name)

    if item == wx.NOT_FOUND:
      return

    r = wx.Rect(*rect)
    r.Deflate(20,20)
    if (item == 0):
      png = wx.Image('/home/irisuser/iris/compositionAdornment.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
      dc.DrawBitmap(png,r.x,r.y)
    elif (item == 1):
      png = wx.Image('/home/irisuser/iris/aggregationAdornment.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
      dc.DrawBitmap(png,r.x,r.y)
    elif (item == 2):
      png = wx.Image('/home/irisuser/iris/associationAdornment.png',wx.BITMAP_TYPE_PNG).ConvertToBitmap()
      dc.DrawBitmap(png,r.x,r.y)
