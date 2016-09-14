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
from cairis.core.Borg import Borg
from cairis.core.ARM import *
import gtk
import math
import cairo
import pangocairo
from cairis.core.armid import *
from KaosModel import KaosModel
from AssetModel import AssetModel
from ConceptMapModel import ConceptMapModel
from LocationModel import LocationModel
from RequirementShape import RequirementShape
import sys

__author__ = 'Shamal Faily'

class KaosTextShape(xdot.TextShape):

    def __init__(self, pen, x, y, j, w, t,modelType,dim,toDim,cSet = False):
        xdot.TextShape.__init__(self,pen,x,y,j,w,t)
        self.fromDim = dim
        self.toDim = toDim
        self.theModelType = modelType
        if (dim == 'persona') or (dim == 'attacker') or ((dim == 'requirement') and cSet == True):
          self.y = y + 22

    def draw(self, cr, highlight=False,zoom_ratio=-1):
        if (((self.fromDim == 'task' and self.toDim == 'asset') or (self.fromDim == 'usecase' and self.toDim == 'asset') or (self.fromDim == 'misusecase' and self.toDim == 'asset') or (self.theModelType == 'task' and self.fromDim == 'asset') or (self.fromDim == 'comment') or (self.fromDim == 'goalconcern') or (self.fromDim == 'obstacleconcern') or (self.fromDim == 'taskconcern')) and (zoom_ratio < MEDKAOS_ZOOM_RATIO)) or (self.fromDim == 'task' and self.toDim == 'misusecase' and zoom_ratio < LOWKAOS_ZOOM_RATIO) :
          pass
        else:
          xdot.TextShape.draw(self,cr,highlight,-1)

class KaosLineShape(xdot.LineShape):
    def __init__(self,pen,points):
        xdot.LineShape.__init__(self,pen,points)
        self.fromDim = ''
        self.toDim = ''
        self.assocType = ''

    def setDimensions(self,fromDim,toDim,assocType):
        self.fromDim = fromDim
        self.toDim = toDim
        self.assocType = assocType

    def draw(self,cr,highlight=False,zoom_ratio=-1): 
        if (((self.fromDim == 'comment') or (self.fromDim == 'goalconcern') or (self.fromDim == 'obstacleconcern') or (self.fromDim == 'taskconcern') ) and (zoom_ratio < MEDKAOS_ZOOM_RATIO)) :
          pass
        else:
          xdot.LineShape.draw(self,cr,highlight,-1)

class KaosBezierShape(xdot.BezierShape):
    def __init__(self,pen,points,filled=False):
        xdot.BezierShape.__init__(self,pen,points,filled)
        self.fromDim = ''
        self.toDim = ''
        self.assocType = ''

    def setDimensions(self,fromDim,toDim,assocType):
        self.fromDim = fromDim
        self.toDim = toDim
        self.assocType = assocType

    def draw(self, cr, highlight=False,zoom_ratio=-1):
        if (((self.fromDim == 'task' and self.toDim == 'asset') or (self.fromDim == 'misusecase' and self.toDim == 'asset') or (self.fromDim == 'comment') or (self.fromDim == 'goalconcern') or (self.fromDim == 'obstacleconcern') or (self.fromDim == 'taskconcern')) and (zoom_ratio < MEDKAOS_ZOOM_RATIO)) or (self.fromDim == 'task' and self.toDim == 'misusecase' and zoom_ratio < LOWKAOS_ZOOM_RATIO) :
          pass
        else:
          xdot.BezierShape.draw(self,cr,highlight,-1)

class KaosEllipseShape(xdot.EllipseShape):
    def __init__(self, pen, x0, y0, w, h, filled=False):
      xdot.EllipseShape.__init__(self,pen,x0,y0,w,h,filled)

    def draw(self, cr, highlight=False,zoom_ratio=-1):
      xdot.EllipseShape.draw(self,cr,highlight,-1)
    

class AttackerShape(xdot.Shape):
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
        cr.set_source_rgb(0,0,0)
        cr.translate(self.x0, self.y0)
        cr.scale(self.w, self.h)
        cr.rectangle(-0.25,-1.05,0.5,0.25)
        cr.fill()
        #hat
        cr.new_path()
        cr.move_to(-0.5,-0.8)
        cr.line_to(0.5,-0.8)

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

class DependShape(xdot.Shape):
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

        cr.move_to(0,-1.25)
        cr.line_to(-1.0,-1.25)
        cr.line_to(-1.0,0.75)
        cr.line_to(0,0.75)
        cr.new_sub_path()
        a1 = 270 * (math.pi / 180)
        a2 = 90 * (math.pi / 180)
        cr.arc(0,-0.25,1,a1,a2)

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

class KaosPolygonShape(xdot.PolygonShape):
    def __init__(self, modelType,dimName,assocType,pen, points, filled=False):
      xdot.PolygonShape.__init__(self,pen,points,filled)
      self.dim = dimName
      self.assocType = assocType
      self.theModelType = modelType

    def draw(self,cr,highlight=False,zoom_ratio=-1):
      if (((self.theModelType == 'task' and self.dim == 'asset') or (self.theModelType == 'class' and self.dim == 'comment') or (self.theModelType == 'class' and self.dim == 'goalconcern') or (self.theModelType == 'class' and self.dim == 'obstacleconcern') or (self.theModelType == 'class' and self.dim == 'taskconcern') ) and (zoom_ratio < MEDKAOS_ZOOM_RATIO)) or (self.assocType in ('taskmisusecasethreat_association','taskmisusecasevulnerability_association','taskmisusecasemitigation_association') and zoom_ratio < LOWKAOS_ZOOM_RATIO) or (self.assocType in ('misusecasethreatasset_association','misusecasevulnerabilityasset_association','misusecasethreatmitigation_association','misusecasevulnerabilitymitigation_association','taskasset_association') and zoom_ratio < MEDKAOS_ZOOM_RATIO) :
        pass
      else:
        xdot.PolygonShape.draw(self,cr,highlight,-1)

class ConflictShape(xdot.Shape):
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
        cr.set_source_rgb(255,0,0)
        cr.translate(self.x0, self.y0)
        cr.scale(self.w, self.h)

        cr.move_to(0.0,-1)
#        cr.new_sub_path()
        cr.line_to(-1,0)
        cr.line_to(1,0)
        cr.line_to(0,1)
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

class KaosXDotAttrParser(xdot.XDotAttrParser):
    def __init__(self,parser, buf,modelType='',dimObjt=None):
      xdot.XDotAttrParser.__init__(self,parser,buf)
      b = Borg()
      self.dbProxy = b.dbProxy
      self.dim = ''
      self.toDim = ''
      self.assocType = ''
      self.objt = ''
      self.cfSet = False
      self.theModelType = modelType
      if (dimObjt != None):
        self.dim = dimObjt[0]
        if (len(dimObjt) == 2):
          self.objt = dimObjt[1]
        elif (len(dimObjt) > 2):
          self.toDim = dimObjt[1]
          self.assocType = dimObjt[2]


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
      self.shapes.append(KaosTextShape(self.pen, x, y, j, w, t,self.theModelType,self.dim,self.toDim,self.cfSet))

    def handle_ellipse(self, x0, y0, w, h, filled=False):
      if (self.dim == 'attacker'):
        if filled:
          self.shapes.append(AttackerShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(AttackerShape(self.pen, x0, y0, w, h))
      elif (self.dim == 'persona'):
        if filled:
          self.shapes.append(PersonaShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(PersonaShape(self.pen, x0, y0, w, h))
      elif (self.dim == 'role' and self.theModelType == 'task'):
        if filled:
          self.shapes.append(PersonaShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(PersonaShape(self.pen, x0, y0, w, h))
      elif (self.dim == 'linkconflict'):
        if filled:
          self.shapes.append(ConflictShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(ConflictShape(self.pen, x0, y0, w, h))
      elif (self.dim == 'depend'):
        if filled:
          self.shapes.append(DependShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(DependShape(self.pen, x0, y0, w, h))
      elif (self.dim == 'requirement' and self.cfSet == True):
        if filled:
          self.shapes.append(RequirementShape(self.pen, x0, y0, w, h,self.objt,self.dbProxy,filled=True))
        self.shapes.append(RequirementShape(self.pen, x0, y0, w, h,self.objt,self.dbProxy))
      else:
        if filled:
          self.shapes.append(KaosEllipseShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(KaosEllipseShape(self.pen, x0, y0, w, h))

    def handle_line(self, points):
        lineShape = KaosLineShape(self.pen, points)
        lineShape.setDimensions(self.dim,self.toDim,self.assocType)
        self.shapes.append(lineShape)

    def handle_bezier(self, points, filled=False):
        if filled:
            filledShape = KaosBezierShape(self.pen, points, filled=True)
            filledShape.setDimensions(self.dim,self.toDim,self.assocType)
            self.shapes.append(filledShape)
        nonFilledShape = KaosBezierShape(self.pen, points)
        nonFilledShape.setDimensions(self.dim,self.toDim,self.assocType)
        self.shapes.append(nonFilledShape)

    def handle_polygon(self, points, filled=False):
        if filled:
            # xdot uses this to mean "draw a filled shape with an outline"
            self.shapes.append(KaosPolygonShape(self.theModelType,self.dim,self.assocType,self.pen, points, filled=True))
        self.shapes.append(KaosPolygonShape(self.theModelType,self.dim,self.assocType,self.pen, points))




class KaosXDotParser(xdot.XDotParser):

    def __init__(self, modelType,xdotcode):
        xdot.XDotParser.__init__(self,xdotcode)
        self.theModelType = modelType
        self.cfSet = False

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
                parser = KaosXDotAttrParser(self,attrs[attr],self.theModelType)
                if (self.theModelType == 'conceptmap'):
                  parser.cfSet = self.cfSet
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
                parser = KaosXDotAttrParser(self,attrs[attr],self.theModelType,dimObjt)
                if (self.theModelType == 'conceptmap'):
                  parser.cfSet = self.cfSet
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
                parser = KaosXDotAttrParser(self,attrs[attr],self.theModelType,dimObjt)
                if (self.theModelType == 'conceptmap'):
                  parser.cfSet = self.cfSet
                shapes.extend(parser.parse())
        if shapes:
            src = self.node_by_name[src_id]
            dst = self.node_by_name[dst_id]
            self.edges.append(xdot.Edge(src, dst, points, shapes))


class KaosDotWidget(xdot.DotWidget):
  def __init__(self):
    xdot.DotWidget.__init__(self)
    self.cfSet = False

  def set_xdotcode(self,modelType, xdotcode):
    parser = KaosXDotParser(modelType,xdotcode)
    if (modelType == 'conceptmap'):
      parser.cfSet = self.cfSet
   
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



class KaosDotWindow(gtk.Window):
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

    def __init__(self,windowTitle,modelType,locsName = ''):
        gtk.Window.__init__(self)
        b = Borg()
        self.dbProxy = b.dbProxy
        self.theModelType = modelType
        self.graph = xdot.Graph()
        self.theLocationsName = locsName
        window = self

        window.set_title(windowTitle)
        if windowTitle != '':
          self.environment = self.dbProxy.dimensionObject(windowTitle,'environment')
        else:
          self.environment = ''
        window.set_default_size(512, 512)
        vbox = gtk.VBox()
        window.add(vbox)

        self.widget = KaosDotWidget()

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
        environmentFrame = gtk.Frame()
        environmentFrame.set_label("Environment")
        environmentFrame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        cBox.pack_start(environmentFrame)
        self.environmentCombo = gtk.ComboBoxEntry()
        environmentFrame.add(self.environmentCombo)
        if (self.theModelType in ('goal','obstacle','task','responsibility','class','conceptmap')):
          sgFrame = gtk.Frame()
          if (self.theModelType == 'goal'):
            sgFrame.set_label("Goal")
          elif (self.theModelType == 'obstacle'):
            sgFrame.set_label("Obstacle")
          elif (self.theModelType == 'task'):
            sgFrame.set_label("Task")
          elif (self.theModelType == 'class'):
            sgFrame.set_label("Asset")
          elif (self.theModelType == 'conceptmap'):
            sgFrame.set_label("Requirement")
          else:
            sgFrame.set_label("Role")
          sgFrame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
          cBox.pack_start(sgFrame)
          self.goalCombo = gtk.ComboBoxEntry()
          sgFrame.add(self.goalCombo)

        # Filter by Misuse Cases in task model as well
        if (self.theModelType == 'task' or self.theModelType == 'goal'):
          sgFrame = gtk.Frame()
          if (self.theModelType == 'task'):
            sgFrame.set_label("Misuse Case")
          else:
            sgFrame.set_label("Use Case")
          sgFrame.set_shadow_type(gtk.SHADOW_ETCHED_IN)
          cBox.pack_start(sgFrame)
          self.caseCombo = gtk.ComboBoxEntry()
          sgFrame.add(self.caseCombo)
        

        #Allow concerns to be hidden for asset models
        if (self.theModelType == 'class'):
          self.hideCheck = gtk.CheckButton("Hide concerns") 
          self.hideCheck.connect("toggled",self.onHideConcerns)
          cBox.pack_start(self.hideCheck)
        elif (self.theModelType == 'goal'):
          self.hideCheck = gtk.CheckButton("Top Level Goals") 
          self.hideCheck.connect("toggled",self.onHideConcerns)
          self.hideCheck.set_sensitive(False)
          cBox.pack_start(self.hideCheck)
        elif (self.theModelType == 'obstacle'):
          self.hideCheck = gtk.CheckButton("Top Level Obstacles") 
          self.hideCheck.connect("toggled",self.onHideConcerns)
          self.hideCheck.set_sensitive(False)
          cBox.pack_start(self.hideCheck)
        elif (self.theModelType == 'conceptmap'):
          self.hideCheck = gtk.CheckButton("Show Chernoff Faces") 
          self.hideCheck.connect("toggled",self.onHideConcerns)
          cBox.pack_start(self.hideCheck)

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

        if (self.theModelType == 'goal'):
          self.layoutCombo.set_active(0)
        elif (self.theModelType == 'obstacle'):
          self.layoutCombo.set_active(0)
        elif (self.theModelType == 'class'):
          self.layoutCombo.set_active(0)
        elif (self.theModelType == 'task'):
          self.layoutCombo.set_active(0)
        elif (self.theModelType == 'responsibility'):
          self.layoutCombo.set_active(2)
        elif (self.theModelType == 'conceptmap'):
          self.layoutCombo.set_active(0)
        self.layoutHandlerId = self.layoutCombo.connect('changed',self.onLayoutChange)

        self.set_focus(self.widget)

        self.show_all()

    def loadFilters(self, environments,goals=[],cs=[]):
      environmentModel = gtk.ListStore(str)
      for environment in environments:
        environmentModel.append([environment]) 
      self.environmentCombo.set_model(environmentModel)
      self.environmentCombo.set_text_column(0)
      self.environmentHandlerId = self.environmentCombo.connect('changed',self.onEnvironmentChange)

      if (len(goals) > 0):
        goals = [''] + goals
        goalModel = gtk.ListStore(str)
        for goal in goals:
          goalModel.append([goal]) 
        self.goalCombo.set_model(goalModel)
        self.goalCombo.set_text_column(0)
        self.goalHandlerId = self.goalCombo.connect('changed',self.onGoalChange)

      if (len(cs) > 0):
        cs = [''] + cs
        caseModel = gtk.ListStore(str)
        for case in cs:
          caseModel.append([case]) 
        self.caseCombo.set_model(caseModel)
        self.caseCombo.set_text_column(0)
        self.caseHandlerId = self.caseCombo.connect('changed',self.onCaseChange)
 

    def blockHandlers(self):
      self.environmentCombo.handler_block(self.environmentHandlerId)

    def unblockHandlers(self):
      self.environmentCombo.handler_unblock(self.environmentHandlerId)

    def onEnvironmentChange(self, action):
      self.blockHandlers()
      environmentName = self.environmentCombo.get_active_text()
      self.environment = self.dbProxy.dimensionObject(environmentName,'environment')
      self.refreshModel()
      # should really change list of misuse cases here if we're viewing task models
      self.unblockHandlers()

    def onGoalChange(self, action):
      self.blockHandlers()
      goalName = self.goalCombo.get_active_text()
      if (goalName != ''):
        if (self.theModelType == 'goal'):
          self.goal = self.dbProxy.dimensionObject(goalName,'goal')
          self.hideCheck.set_sensitive(True)
        elif (self.theModelType == 'obstacle'):
          self.goal = self.dbProxy.dimensionObject(goalName,'obstacle')
          self.hideCheck.set_sensitive(True)
        elif (self.theModelType == 'class'):
          self.goal = self.dbProxy.dimensionObject(goalName,'asset')
          self.hideCheck.set_sensitive(True)
        elif (self.theModelType == 'task'):
          self.task = self.dbProxy.dimensionObject(goalName,'task')
        elif (self.theModelType == 'conceptmap'):
          self.task = self.dbProxy.dimensionObject(goalName,'requirement')
        else:
          self.role = self.dbProxy.dimensionObject(goalName,'role')
      else:
        if (self.theModelType in ('goal','obstacle')):
          self.hideCheck.set_active(False)
          self.hideCheck.set_sensitive(False)
      self.refreshModel()
      self.unblockHandlers()

    def onCaseChange(self, action):
      self.blockHandlers()
      self.refreshModel()
      self.unblockHandlers()

    def onHideConcerns(self, action):
      self.blockHandlers()
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
        if self.widget.set_xdotcode(self.theModelType,xdotcode):
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
      goalName = ''
      dimName = ''
      objtName = ''
      caseFilter = False
      environmentIdx = self.environmentCombo.get_active()
      if (environmentIdx != -1):
        environmentName = self.environmentCombo.get_active_text()
      else:
        environmentModel = self.get_title()

      if (self.theModelType in ('goal','obstacle','task','responsibility','class','conceptmap')):
        goalIdx = self.goalCombo.get_active()
        if (goalIdx != -1 and goalIdx != 0):
          goalName = self.goalCombo.get_active_text()

        if (self.theModelType == 'task' or self.theModelType == 'goal'):
          cIdx = self.caseCombo.get_active()
          if (cIdx != -1 and cIdx != 0):
            goalName = self.caseCombo.get_active_text()
            self.goalCombo.set_text_column(0)
            caseFilter = True
        
      try:
        b = Borg()
        proxy = b.dbProxy
        associationDictionary = {}
        if (self.theModelType == 'class'):
          hideConcerns = self.hideCheck.get_active()
          associationDictionary = proxy.classModel(environmentName,goalName,hideConcerns)
          self.canonicalModel = AssetModel(associationDictionary.values(),environmentName,goalName,hideConcerns)
        elif (self.theModelType == 'goal'):
          topLevelGoals = self.hideCheck.get_active()
          associationDictionary = proxy.goalModel(environmentName,goalName,topLevelGoals,caseFilter)
          self.canonicalModel = KaosModel(associationDictionary.values(),environmentName,self.theModelType,goalName)
        elif (self.theModelType == 'obstacle'):
          topLevelGoals = self.hideCheck.get_active()
          associationDictionary = proxy.obstacleModel(environmentName,goalName,topLevelGoals)
          self.canonicalModel = KaosModel(associationDictionary.values(),environmentName,self.theModelType,goalName)
        elif (self.theModelType == 'responsibility'):
          associationDictionary = proxy.responsibilityModel(environmentName,goalName)
          self.canonicalModel = KaosModel(associationDictionary.values(),environmentName,self.theModelType,goalName)
        elif (self.theModelType == 'conceptmap'):
          cfSet = self.hideCheck.get_active()
          associationDictionary = proxy.conceptMapModel(environmentName,goalName)
          self.canonicalModel = ConceptMapModel(associationDictionary.values(),environmentName,self.theModelType,cfSet)
          self.widget.cfSet = cfSet
        elif (self.theModelType == 'location'):
          riskOverlay = proxy.locationsRiskModel(self.theLocationsName,environmentName)
          self.canonicalModel = LocationModel(self.theLocationsName,environmentName,riskOverlay)
        else:
          associationDictionary = proxy.taskModel(environmentName,goalName,caseFilter)
          self.canonicalModel = KaosModel(associationDictionary.values(),environmentName,self.theModelType,goalName)

        self.set_xdotcode(self.canonicalModel.graph())
        self.widget.zoom_to_fit()
        self.set_title(environmentName)
      except ARMException, ex:
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
        if (len(fileNameComponents) == 1):
          fileType = 'pdf'
        else:
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


    def reloadFilters(self,envName):
      environmentNames = self.dbProxy.getDimensionNames('environment')
      environmentNames.sort(key=str.lower)

      if (self.modelType == 'goal'):
        goalNames = self.dbProxy.environmentGoals(envName)
        goalNames.sort(key=str.lower)
        ucNames = self.dbProxy.environmentUseCases(envName)
        ucNames.sort(key=str.lower)
        self.loadFilters(environmentNames,goalNames,ucNames)
      elif (self.modelType == 'obstacle'):
        obsNames = self.dbProxy.environmentObstacles(envName)
        obsNames.sort(key=str.lower)
        self.loadFilters(environmentNames,obsNames)
      elif (self.modelType == 'class'):
        asNames = self.dbProxy.environmentAssets(envName)
        asNames.sort(key=str.lower)
        self.loadFilters(environmentNames,asNames)
      elif (self.modelType == 'conceptmap'):
        asNames = self.dbProxy.environmentRequirements(envName)
        asNames.sort(key=str.lower)
        self.loadFilters(environmentNames,asNames)
      elif (self.modelType == 'task'):
        taskNames = self.dbProxy.environmentTasks(envName)
        mcNames = self.dbProxy.getDimensionNames('misusecase')
        taskNames.sort(key=str.lower)
        self.loadFilters(environmentNames,taskNames,mcNames)
      elif (self.modelType == 'responsibility'):
        roleNames = self.dbProxy.getDimensionNames('role')
        roleNames.sort(key=str.lower)
        self.loadFilters(environmentNames,roleNames)
      else:
        self.loadFilters(environmentNames)
