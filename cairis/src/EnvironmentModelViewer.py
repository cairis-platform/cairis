#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/EnvironmentModelViewer.py $ $Id: EnvironmentModelViewer.py 299 2010-07-12 07:31:50Z shaf $
import gtk
import gtk.gdk
from envxdot import EnvironmentDotWindow
from ARM import *
import NodeDialogFactory

class EnvironmentModelViewer(EnvironmentDotWindow):
  def __init__(self,environmentName,dp):
    EnvironmentDotWindow.__init__(self,environmentName,dp)
    self.dbProxy = dp
    self.environment = self.dbProxy.dimensionObject(environmentName,'environment')
    self.widget.connect('clicked', self.on_url_clicked)
    self.widget.connect('button_press_event', self.onClick)

  def onClick(self,widget,event):
    try:
      if event.button == 3:
        print self.widget.get_url(event.x,event.y).url
      return 1
    except AttributeError:
      pass
 
  def on_url_clicked(self, widget, url, event):
    dialog = NodeDialogFactory.build(url,self.environment.name())
    return True

  def onTypeClicked(self, widget, event):
    pass

  def onNameClicked(self, widget, event):
    pass

  def ShowModal(self, tLinks):
    self.updateModel(tLinks)
    self.connect('destroy', gtk.main_quit)
    self.set_modal(True)
    gtk.main()

  def updateModel(self,tLinks):
    self.traceModel = tLinks
    xdotcode = self.traceModel.graph()
    environmentNames = self.dbProxy.getDimensionNames('environment')
    environmentNames.sort(key=str.lower)
    self.loadFilters(environmentNames,tLinks.dimensions(),tLinks.objects())
    self.set_xdotcode(xdotcode)
    self.blockHandlers()
    self.environmentCombo.set_active(environmentNames.index(self.environment.name()))
    self.unblockHandlers()
    self.widget.zoom_to_fit()
