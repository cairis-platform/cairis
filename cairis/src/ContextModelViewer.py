#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ContextModelViewer.py $ $Id: ContextModelViewer.py 249 2010-05-30 17:07:31Z shaf $
import gtk
import gtk.gdk
import contextxdot
import ContextNodeDialogFactory
import os

class ContextModelViewer(contextxdot.ContextDotWindow):
  def __init__(self,environmentName,dp):
    contextxdot.ContextDotWindow.__init__(self,environmentName,dp)
    self.dbProxy = dp
    if (environmentName != ''):
      self.environment = self.dbProxy.dimensionObject(environmentName,'environment')
    else:
      self.environment = None
    self.widget.connect('clicked', self.on_url_clicked)
    self.widget.connect('button_press_event', self.onClick)

    directoryPrefix = ''
    if (os.name == 'nt'):
      directoryPrefix += 'C:\\iris\\'
    elif (os.uname()[0] == 'Linux'):
      directoryPrefix += os.environ['IRIS_IMAGES'] + '/'
    elif (os.uname()[0] == 'Darwin'):
      directoryPrefix += os.environ['IRIS_IMAGES'] + '/'
    else:
      raise UnsupportedOperatingSystem(os.name)

    self.set_icon_from_file(directoryPrefix + 'contextModel.png')

  def onClick(self,widget,event):
    if event.button == 3:
      print 'right clicked ', self.widget.get_url(event.x,event.y).url
    return 1
 
  def on_url_clicked(self, widget, url, event):
    urlElements = url.split('#')
    if (urlElements[0] != 'link'):
      dialog = ContextNodeDialogFactory.build(url)
    return True

  def onTypeClicked(self, widget, event):
    pass

  def onNameClicked(self, widget, event):
    pass

  def ShowModal(self, associations):
    self.updateModel(associations)
    self.connect('destroy', gtk.main_quit)
    gtk.main()

  def updateModel(self,associations):
    self.canonicalModel = associations
    xdotcode = self.canonicalModel.graph()
    self.set_xdotcode(xdotcode)
    self.widget.zoom_to_fit()

  def updateModel(self,associations):
    self.canonicalModel = associations
    xdotcode = self.canonicalModel.graph()
    environmentNames = [''] + self.dbProxy.getDimensionNames('environment')
    environmentNames.sort(key=str.lower)
    self.loadFilters(environmentNames)
    self.set_xdotcode(xdotcode)
    self.blockHandlers()
    if (self.environment != None):
      self.environmentCombo.set_active(environmentNames.index(self.environment.name()))
    self.unblockHandlers()
    self.widget.zoom_to_fit()

