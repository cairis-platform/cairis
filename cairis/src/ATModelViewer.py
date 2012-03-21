#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/APModelViewer.py $ $Id: APModelViewer.py 330 2010-10-31 15:01:28Z shaf $
import gtk
import gtk.gdk
import atxdot
import AssumptionNodeDialogFactory
import os
from ARM import *
from Borg import Borg

class ATModelViewer(atxdot.ATDotWindow):
  def __init__(self,tName = ''):
    atxdot.ATDotWindow.__init__(self)
    b = Borg()
    self.dbProxy = b.dbProxy
    self.theInitialTask = tName
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

    self.set_icon_from_file(directoryPrefix + 'atModel.png')


  def on_url_clicked(self, widget, url, event):
    self.url = url
    urlElements = url.split('#')
    if (urlElements[0] != 'link'):
      dialog = AssumptionNodeDialogFactory.build(url,False)
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

      taskNames = self.dbProxy.getDimensionNames('task')
      charNames = self.canonicalModel.taskCharacteristics

      self.loadFilters(taskNames,charNames)
      self.set_xdotcode(xdotcode)
      self.widget.zoom_to_fit()
    except ARMException,errorText:
      print str(errorText)
#      dlg = wx.MessageDialog(self,str(errorText),'IRIS',wx.OK | wx.ICON_ERROR)
#      dlg.ShowModal()
#      dlg.Destroy()
#      return
