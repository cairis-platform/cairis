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
import armid
from AssumptionPersonaModel import AssumptionPersonaModel

class APTextShape(xdot.TextShape):

    def __init__(self, pen, x, y, j, w, t,dim,toDim):
        xdot.TextShape.__init__(self,pen,x,y,j,w,t)
        self.fromDim = dim
        self.toDim = toDim
        if (dim == 'persona') or (dim == 'attacker'):
          self.y = y + 22

    def draw(self, cr, highlight=False,zoom_ratio=-1):
        xdot.TextShape.draw(self,cr,highlight,-1)

class APLineShape(xdot.LineShape):
    def __init__(self,pen,points):
        xdot.LineShape.__init__(self,pen,points)
        self.fromDim = ''
        self.toDim = ''

    def setDimensions(self,fromDim,toDim):
        self.fromDim = fromDim
        self.toDim = toDim

    def draw(self,cr,highlight=False,zoom_ratio=-1): 
        xdot.LineShape.draw(self,cr,highlight,-1)

class APBezierShape(xdot.BezierShape):
    def __init__(self,pen,points,filled=False):
        xdot.BezierShape.__init__(self,pen,points,filled)
        self.fromDim = ''
        self.toDim = ''

    def setDimensions(self,fromDim,toDim):
        self.fromDim = fromDim
        self.toDim = toDim

    def draw(self, cr, highlight=False,zoom_ratio=-1):
        xdot.BezierShape.draw(self,cr,highlight,-1)

class APEllipseShape(xdot.EllipseShape):
    def __init__(self, pen, x0, y0, w, h, filled=False):
      xdot.EllipseShape.__init__(self,pen,x0,y0,w,h,filled)

    def draw(self, cr, highlight=False,zoom_ratio=-1):
      xdot.EllipseShape.draw(self,cr,highlight,-1)
    

class PersonaShape(xdot.Shape):
    def __init__(self, pen, x0, y0, w, h, filled=False):
        xdot.Shape.__init__(self)
        self.pen = pen.copy()
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h
        self.filled = filled

    def draw(self, cr, highlight=False,zoom_ratio=-1):
        cr.save()
        cr.translate(self.x0, self.y0)
        cr.scale(self.w, self.h)

        cr.move_to(0.0,0.0)
        cr.line_to(0.0,-0.5)
        cr.new_sub_path()
        cr.arc(0.0,-0.75,0.25,0,2.0 * math.pi)
        cr.move_to(0.0,0.0)
        cr.line_to(0.0,0.25)
        cr.line_to(-0.4,0.9)
        cr.move_to(0.0,0.25)
        cr.line_to(0.4,0.9)
        cr.move_to(-0.4,-0.2)
        cr.line_to(0.4,-0.2)

        cr.restore()
        pen = self.select_pen(highlight)
        if self.filled:
            cr.set_source_rgba(*pen.fillcolor)
            cr.fill()
        else:
            cr.set_dash(pen.dash)
            cr.set_line_width(pen.linewidth)
            cr.set_source_rgba(*pen.color)
            cr.stroke()

class APPolygonShape(xdot.PolygonShape):
    def __init__(self, dimName,pen, points, filled=False):
      xdot.PolygonShape.__init__(self,pen,points,filled)
      self.dim = dimName

    def draw(self,cr,highlight=False,zoom_ratio=-1):
      xdot.PolygonShape.draw(self,cr,highlight,-1)

class APXDotAttrParser(xdot.XDotAttrParser):
    def __init__(self,parser, buf,dimObjt=None):
      xdot.XDotAttrParser.__init__(self,parser,buf)
      self.dim = ''
      self.toDim = ''
      if (dimObjt != None):
        self.dim = dimObjt[0]
        if (len(dimObjt) > 2):
          self.toDim = dimObjt[1]


    def parse(self):
        s = self

        while s:
            op = s.read_code()
            if op == "c":
                color = s.read_color()
                if color is not None:
                    self.handle_color(color, filled=False)
            elif op == "C":
                color = s.read_color()
                if color is not None:
                    self.handle_color(color, filled=True)
            elif op == "S":
                # http://www.graphviz.org/doc/info/attrs.html#k:style
                style = s.read_text()
                if style.startswith("setlinewidth("):
                    lw = style.split("(")[1].split(")")[0]
                    lw = float(lw)
                    self.handle_linewidth(lw)
                elif style in ("solid", "dashed"):
                    self.handle_linestyle(style)
            elif op == "F":
                size = s.read_float()
                name = s.read_text()
                self.handle_font(size, name)
            elif op == "T":
                x, y = s.read_point()
                j = s.read_number()
                w = s.read_number()
                t = s.read_text()
                self.handle_text(x, y, j, w, t)
            elif op == "E":
                x0, y0 = s.read_point()
                w = s.read_number()
                h = s.read_number()
                self.handle_ellipse(x0, y0, w, h, filled=True)
            elif op == "e":
                x0, y0 = s.read_point()
                w = s.read_number()
                h = s.read_number()
                self.handle_ellipse(x0, y0, w, h, filled=False)
            elif op == "L":
                points = self.read_polygon()
                self.handle_line(points)
            elif op == "B":
                points = self.read_polygon()
                self.handle_bezier(points, filled=False)
            elif op == "b":
                points = self.read_polygon()
                self.handle_bezier(points, filled=True)
            elif op == "P":
                points = self.read_polygon()
                self.handle_polygon(points, filled=True)
            elif op == "p":
                points = self.read_polygon()
                self.handle_polygon(points, filled=False)
            else:
                sys.stderr.write("unknown xdot opcode '%s'\n" % op)
                break

        return self.shapes


    def handle_text(self,x,y,j,w,t):
      self.shapes.append(APTextShape(self.pen, x, y, j, w, t,self.dim,self.toDim))

    def handle_ellipse(self, x0, y0, w, h, filled=False):
      if (self.dim == 'persona'):
        if filled:
          self.shapes.append(PersonaShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(PersonaShape(self.pen, x0, y0, w, h))
      else:
        if filled:
          self.shapes.append(APEllipseShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(APEllipseShape(self.pen, x0, y0, w, h))

    def handle_line(self, points):
        lineShape = APLineShape(self.pen, points)
        lineShape.setDimensions(self.dim,self.toDim)
        self.shapes.append(lineShape)

    def handle_bezier(self, points, filled=False):
        if filled:
            filledShape = APBezierShape(self.pen, points, filled=True)
            filledShape.setDimensions(self.dim,self.toDim)
            self.shapes.append(filledShape)
        nonFilledShape = APBezierShape(self.pen, points)
        nonFilledShape.setDimensions(self.dim,self.toDim)
        self.shapes.append(nonFilledShape)

    def handle_polygon(self, points, filled=False):
        if filled:
            # xdot uses this to mean "draw a filled shape with an outline"
            self.shapes.append(APPolygonShape(self.dim,self.pen, points, filled=True))
        self.shapes.append(APPolygonShape(self.dim,self.pen, points))




class APXDotParser(xdot.XDotParser):

    def __init__(self, xdotcode):
        xdot.XDotParser.__init__(self,xdotcode)

    def handle_graph(self, attrs):
        if self.top_graph:
            try:
                bb = attrs['bb']
            except KeyError:
                return

            if not bb:
                return

            xmin, ymin, xmax, ymax = map(float, bb.split(","))

            self.xoffset = -xmin
            self.yoffset = -ymax
            self.xscale = 1.0
            self.yscale = -1.0
            # FIXME: scale from points to pixels

            self.width = xmax - xmin
            self.height = ymax - ymin

            self.top_graph = False

        for attr in ("_draw_", "_ldraw_", "_hdraw_", "_tdraw_", "_hldraw_", "_tldraw_"):
            if attr in attrs:
                parser = APXDotAttrParser(self,attrs[attr])
                self.shapes.extend(parser.parse())

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
                parser = APXDotAttrParser(self,attrs[attr],dimObjt)
                shapes.extend(parser.parse())
        url = attrs.get('URL', None)
        node = xdot.Node(x, y, w, h, shapes, url)
        self.node_by_name[id] = node
        if shapes:
            self.nodes.append(node)

    def handle_edge(self, src_id, dst_id, attrs):
        try:
            pos = attrs['pos']
        except KeyError:
            return

        points = self.parse_edge_pos(pos)
        shapes = []
        for attr in ("_draw_", "_ldraw_", "_hdraw_", "_tdraw_", "_hldraw_", "_tldraw_"):
            if attr in attrs:
                dimObjt = ['','']
                try:
                  dimObjt = (attrs['URL']).split('#')
                except KeyError:
                  pass
                parser = APXDotAttrParser(self,attrs[attr],dimObjt)
                shapes.extend(parser.parse())
        if shapes:
            src = self.node_by_name[src_id]
            dst = self.node_by_name[dst_id]
            self.edges.append(xdot.Edge(src, dst, points, shapes))


class APDotWidget(xdot.DotWidget):
  def __init__(self):
    xdot.DotWidget.__init__(self)

  def set_xdotcode(self,xdotcode):
    parser = APXDotParser(xdotcode)
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



class APDotWindow(gtk.Window):
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

    def __init__(self):
        gtk.Window.__init__(self)
        b = Borg()
        self.dbProxy = b.dbProxy
        self.graph = xdot.Graph()

        window = self

        window.set_title('Assumption Persona model')
        window.set_default_size(512, 512)
        vbox = gtk.VBox()
        window.add(vbox)

        self.widget = APDotWidget()

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


        # add start
        cBox = gtk.HBox()
        vbox.pack_start(cBox,False)
        personaFrame = gtk.Frame()
        personaFrame.set_label("Persona")
        personaFrame.set_shadow_type(gtk.SHADOW_ETCHED_IN)

        cBox.pack_start(personaFrame)
        self.personaCombo = gtk.ComboBoxEntry()
        personaFrame.add(self.personaCombo)

        btFrame = gtk.Frame()
        btFrame.set_label("Behaviour Type")
        btFrame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        cBox.pack_start(btFrame)
        self.btCombo = gtk.ComboBoxEntry()
        btFrame.add(self.btCombo)

        charFrame = gtk.Frame()
        charFrame.set_label("Characteristic")
        charFrame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        cBox.pack_start(charFrame)
        self.charCombo = gtk.ComboBoxEntry()
        charFrame.add(self.charCombo)

        # add end
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

    def loadFilters(self,personas=[],btTypes=[],chars=[]):
      personaModel = gtk.ListStore(str)
      pIdx = 0
      personaModel.append([''])
      for pidx,persona in enumerate(personas):
        if (persona == self.theInitialPersona):
          pIdx = pidx + 1
          self.theInitialPersona = ''
        personaModel.append([persona]) 
      self.personaCombo.set_model(personaModel)
      self.personaCombo.set_text_column(0)
      self.personaCombo.set_active(pIdx)
      self.personaHandlerId = self.personaCombo.connect('changed',self.onPersonaChange)

      btIdx = 0
      btModel = gtk.ListStore(str)
      btModel.append([''])
      for bidx,bt in enumerate(btTypes):
        if (bt == self.theInitialBv):
          btIdx = bidx + 1
          self.theInitialBv = ''
        btModel.append([bt]) 
      self.btCombo.set_model(btModel)
      self.btCombo.set_text_column(0)
      self.btCombo.set_active(btIdx)
      self.btHandlerId = self.btCombo.connect('changed',self.onBTypeChange)

      charModel = gtk.ListStore(str)
      charModel.append([''])
      for pc in chars:
        charModel.append([pc]) 
      self.charCombo.set_model(charModel)
      self.charCombo.set_text_column(0)
      self.charHandlerId = self.charCombo.connect('changed',self.onCharChange)

    def onPersonaChange(self, action):
      personaName = self.personaCombo.get_active_text()
      self.refreshModel(personaName,'','')

      self.charCombo.set_model(self.canonicalModel.characteristics())
      self.btCombo.set_active(0)
      self.charCombo.set_active(0)

    def onBTypeChange(self, action):
      personaName = self.personaCombo.get_active_text()
      btName = self.btCombo.get_active_text()
      self.refreshModel(personaName,btName,'')

      self.charCombo.set_model(self.canonicalModel.characteristics())
      self.charCombo.set_active(0)


    def onCharChange(self, action):
      personaName = self.personaCombo.get_active_text()
      btName = self.btCombo.get_active_text()
      charName = self.charCombo.get_active_text()
      self.refreshModel(personaName,btName,charName)
      
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

    def refreshModel(self,personaName,btName,charName):
      try:
        b = Borg()
        proxy = b.dbProxy
        associationDictionary = {}
        associations = proxy.assumptionPersonaModel(personaName,btName,charName)
        self.canonicalModel = AssumptionPersonaModel(associations)

        self.set_xdotcode(self.canonicalModel.graph())
        self.widget.zoom_to_fit()
        self.set_title('Assumption Persona Model')
      except ARM.ARMException, ex:
        dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,message_format=str(ex),buttons=gtk.BUTTONS_OK)
        dlg.set_title('Model Viewer')
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
            dlg.set_title('Environment Model Viewer')
            dlg.run()
            dlg.destroy()
        else:
          self.widget.printToFile(fileName,fileType)
      else:
        chooser.destroy()
