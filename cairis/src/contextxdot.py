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


import xdot
from Borg import Borg
import ARM
import gtk
import math
import cairo
import pangocairo
from ContextModel import ContextModel

class MachineShape(xdot.PolygonShape):
  def __init__(self, pen, points, filled=False):
    xdot.PolygonShape.__init__(self,pen,points,filled)

  def draw(self, cr, highlight=False,zoom_ratio = -1):
    xdot.PolygonShape.draw(self,cr,highlight=False,zoom_ratio = -1)

    xs = self.points[0][0]
    xe = self.points[3][0]
    ys = self.points[1][1]
    ye = self.points[2][1]
    cr.move_to(xs + 4,ye)
    cr.line_to(xs + 4,self.points[0][1])
    cr.move_to(xs + 8,ye)
    cr.line_to(xs + 8,self.points[0][1])
    cr.stroke()

class DesignedDomainShape(xdot.PolygonShape):
  def __init__(self, pen, points, filled=False):
    xdot.PolygonShape.__init__(self,pen,points,filled)

  def draw(self, cr, highlight=False,zoom_ratio = -1):
    xdot.PolygonShape.draw(self,cr,highlight=False,zoom_ratio = -1)

    xs = self.points[0][0]
    xe = self.points[3][0]
    ys = self.points[1][1]
    ye = self.points[2][1]
    cr.move_to(xs + 4,ye)
    cr.line_to(xs + 4,self.points[0][1])
    cr.stroke()

class XDotAttrParser(xdot.XDotAttrParser):
  def __init__(self, parser, buf,dim=''):
    xdot.XDotAttrParser.__init__(self,parser,buf)
    self.dim = dim

  def handle_polygon(self, points, filled=False):
   if (self.dim == 'machine'):
     if filled:
       self.shapes.append(MachineShape(self.pen, points, filled=True))
     self.shapes.append(MachineShape(self.pen, points))
   elif (self.dim == 'designeddomain'):
     if filled:
       self.shapes.append(DesignedDomainShape(self.pen, points, filled=True))
     self.shapes.append(DesignedDomainShape(self.pen, points))

   else:
     if filled:
       self.shapes.append(xdot.PolygonShape(self.pen, points, filled=True))
     self.shapes.append(xdot.PolygonShape(self.pen, points))



class XDotParser(xdot.XDotParser):
  def __init__(self, xdotcode):
    xdot.XDotParser.__init__(self,xdotcode)

  def handle_node(self, id, attrs):
    try:
      pos = attrs['pos']
    except KeyError:
      return

    x, y = self.parse_node_pos(pos)
    w = float(attrs['width'])*72
    h = float(attrs['height'])*72
    shapes = []
    for attr in ("_draw_", "_ldraw_"):
      if attr in attrs:
        dimObjt = (attrs['URL']).split('#')
        parser = XDotAttrParser(self, attrs[attr],dimObjt[0])
        shapes.extend(parser.parse())
      url = attrs.get('URL', None)
      node = xdot.Node(x, y, w, h, shapes, url)
      self.node_by_name[id] = node
      if shapes:
        self.nodes.append(node)



class ContextDotWidget(xdot.DotWidget):
  def __init__(self):
    xdot.DotWidget.__init__(self)

  def set_xdotcode(self, xdotcode):
    parser = XDotParser(xdotcode)
    self.graph = parser.parse()
    self.zoom_image(self.zoom_ratio, center=True)

  def printToFile(self,fileName,fileFormat):
    s = None
    if (fileFormat == 'svg'):
      s = cairo.SVGSurface(fileName,self.graph.width,self.graph.height)
    else:
      s = cairo.PDFSurface(fileName,self.graph.width,self.graph.height)

    c1 = cairo.Context(s)
    c2 = pangocairo.CairoContext(c1)
    c2.set_line_cap(cairo.LINE_CAP_BUTT)
    c2.set_line_join(cairo.LINE_JOIN_MITER)

    self.graph.draw(c2)
    s.finish()



class ContextDotWindow(gtk.Window):
    ui = '''
    <ui>
        <toolbar name="ToolBar">
            <toolitem action="Refresh"/>
            <separator/>
            <toolitem action="Print"/>
            <separator/>
            <toolitem action="ZoomIn"/>
            <toolitem action="ZoomOut"/>
            <toolitem action="ZoomFit"/>
            <toolitem action="Zoom100"/>
        </toolbar>
    </ui>
    '''

    def __init__(self,envName,dp):
        gtk.Window.__init__(self)
        self.dbProxy = dp
        self.graph = xdot.Graph()

        window = self

        window.set_title(envName + ' Context Model')
        if (envName != ''):
          self.environment = self.dbProxy.dimensionObject(envName,'environment')
        window.set_default_size(512, 512)
        vbox = gtk.VBox()
        window.add(vbox)

        self.widget = ContextDotWidget()

        # Create a UIManager instance
        uimanager = self.uimanager = gtk.UIManager()

        # Add the accelerator group to the toplevel window
        accelgroup = uimanager.get_accel_group()
        window.add_accel_group(accelgroup)

        # Create an ActionGroup
        actiongroup = gtk.ActionGroup('Actions')
        self.actiongroup = actiongroup

        # Create actions
        actiongroup.add_actions((
            ('Refresh', gtk.STOCK_REFRESH, None, None, None, self.on_refresh),
            ('Print', gtk.STOCK_PRINT, None, None, None, self.on_print),
            ('ZoomIn', gtk.STOCK_ZOOM_IN, None, None, None, self.widget.on_zoom_in),
            ('ZoomOut', gtk.STOCK_ZOOM_OUT, None, None, None, self.widget.on_zoom_out),
            ('ZoomFit', gtk.STOCK_ZOOM_FIT, None, None, None, self.widget.on_zoom_fit),
            ('Zoom100', gtk.STOCK_ZOOM_100, None, None, None, self.widget.on_zoom_100),
        ))

        # Add the actiongroup to the uimanager
        uimanager.insert_action_group(actiongroup, 0)

        # Add a UI descrption
        uimanager.add_ui_from_string(self.ui)

        # Create a Toolbar
        toolbar = uimanager.get_widget('/ToolBar')
        vbox.pack_start(toolbar, False)

        cBox = gtk.HBox()
        vbox.pack_start(cBox,False)
        environmentFrame = gtk.Frame()
        environmentFrame.set_label("Environment")
        environmentFrame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        cBox.pack_start(environmentFrame)
        self.environmentCombo = gtk.ComboBoxEntry()
        environmentFrame.add(self.environmentCombo)

        vbox.pack_start(self.widget)

        lBox = gtk.HBox()
        vbox.pack_start(lBox,False)
        lFrame = gtk.Frame()
        lFrame.set_label("Layout")
        lFrame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        lBox.pack_start(lFrame)
        self.layoutCombo = gtk.ComboBoxEntry()
        lFrame.add(self.layoutCombo)

        layoutModel = gtk.ListStore(str)
        layoutModel.append(['Hierarchical'])
        layoutModel.append(['Spring'])
        layoutModel.append(['Radial'])
        layoutModel.append(['Circular'])
        self.layoutCombo.set_model(layoutModel)
        self.layoutCombo.set_text_column(0)

        self.layoutCombo.set_active(0)
        self.layoutHandlerId = self.layoutCombo.connect('changed',self.onLayoutChange)
        self.set_focus(self.widget)
        self.show_all()

    def loadFilters(self, environments):
      environmentModel = gtk.ListStore(str)
      for environment in environments:
        environmentModel.append([environment])
      self.environmentCombo.set_model(environmentModel)
      self.environmentCombo.set_text_column(0)
      self.environmentHandlerId = self.environmentCombo.connect('changed',self.onEnvironmentChange)

    def blockHandlers(self):
      self.environmentCombo.handler_block(self.environmentHandlerId)

    def unblockHandlers(self):
      self.environmentCombo.handler_unblock(self.environmentHandlerId)

    def onEnvironmentChange(self, action):
      self.blockHandlers()
      environmentName = self.environmentCombo.get_active_text()
      if (environmentName != ''):
        self.environment = self.dbProxy.dimensionObject(environmentName,'environment')
      self.refreshModel()
      self.unblockHandlers()

    def onLayoutChange(self,action):
      layoutName = self.layoutCombo.get_active_text()
      renderer = 'fdp'
      if (layoutName == 'Hierarchical'):
        renderer = 'dot'
      elif (layoutName == 'Radial'):
        renderer = 'twopi'
      elif (layoutName == 'Circular'):
        renderer = 'circo'
  
      self.set_xdotcode(self.canonicalModel.layout(renderer))

    def set_filter(self, filter):
        self.widget.set_filter(filter)

    def set_dotcode(self, dotcode, filename='<stdin>'):
        if self.widget.set_dotcode(dotcode, filename):
            self.set_title(os.path.basename(filename) + ' - Dot Viewer')
            self.widget.zoom_to_fit()

    def set_xdotcode(self, xdotcode, filename='<stdin>'):
        if self.widget.set_xdotcode(xdotcode):
            self.set_title(os.path.basename(filename) + ' - Dot Viewer')
            self.widget.zoom_to_fit()

    def open_file(self, filename):
        try:
            fp = file(filename, 'rt')
            self.set_dotcode(fp.read(), filename)
            fp.close()
        except IOError, ex:
            dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,
                                    message_format=str(ex),
                                    buttons=gtk.BUTTONS_OK)
            dlg.set_title('Dot Viewer')
            dlg.run()
            dlg.destroy()

    def on_refresh(self, action):
      self.refreshModel()

    def refreshModel(self):
      environmentName = ''
      dimName = ''
      objtName = ''
      environmentIdx = self.environmentCombo.get_active()
      if (environmentIdx != -1):
        environmentName = self.environmentCombo.get_active_text()
      else:
        environmentModel = self.get_title()
 
      try:
        b = Borg()
        proxy = b.dbProxy
        self.canonicalModel = proxy.contextModel(environmentName)
        self.set_xdotcode(self.canonicalModel.graph())
        self.widget.zoom_to_fit()
      except ARM.ARMException, ex:
        dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,message_format=str(ex),buttons=gtk.BUTTONS_OK)
        dlg.set_title('Context Model Viewer')
        dlg.run()
        dlg.destroy()

    def on_print(self, action):
      chooser = gtk.FileChooserDialog(title="Print to file",action = gtk.FILE_CHOOSER_ACTION_SAVE,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
      chooser.set_default_response(gtk.RESPONSE_OK)
      filter = gtk.FileFilter()
      filter.set_name('Images')
      filter.add_mime_type('impages/svg')
      filter.add_mime_type('impages/pdf')
      filter.add_pattern('*.svg')
      filter.add_pattern('*.pdf')
      chooser.add_filter(filter)
      if chooser.run() == gtk.RESPONSE_OK:
        fileName =  chooser.get_filename()
        chooser.destroy()
        fileNameComponents = fileName.split('.')
        fileType = fileNameComponents[1]
        if ((fileType != 'svg') and (fileType != 'pdf')):
            dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,message_format='Unknown file type',buttons=gtk.BUTTONS_OK)
            dlg.set_title('Context Model Viewer')
            dlg.run()
            dlg.destroy()
        else:
          self.widget.printToFile(fileName,fileType)
      else:
        chooser.destroy()

