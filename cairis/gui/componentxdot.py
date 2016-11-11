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
from ComponentModel import ComponentModel

__author__ = 'Shamal Faily'

class ComponentTextShape(xdot.TextShape):
  def __init__(self, pen, x, y, j, w, t,dim):
    xdot.TextShape.__init__(self,pen,x,y,j,w,t)

  def draw(self, cr, highlight=False,zoom_ratio=-1):
    xdot.TextShape.draw(self,cr,highlight,zoom_ratio)

class InterfaceLabelShape(xdot.TextShape):
  def __init__(self, pen, x, y, j, w, objtName):
    ifLbls = objtName.split('_')
    xdot.TextShape.__init__(self,pen,x,y,j,w,ifLbls[1])

  def draw(self, cr, highlight=False,zoom_ratio=-1):
    xdot.TextShape.draw(self,cr,highlight,zoom_ratio)


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
      if (zoom_ratio == -1) or (zoom_ratio > HIGH_ZOOM_RATIO):
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
      if (zoom_ratio == -1) or (zoom_ratio > HIGH_ZOOM_RATIO):
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

class RequiredInterfaceShape(xdot.EllipseShape):
    def __init__(self, pen, x0, y0, w, h, objtName, filled=False):
      xdot.EllipseShape.__init__(self,pen,x0,y0,w,h,filled)
      self.theInterfaceName = objtName 

    def draw(self, cr, highlight=False,zoom_ratio=-1):
      cr.save()
      cr.translate(self.x0, self.y0)
      cr.scale(self.w, self.h)
      cr.rotate(0.5 * math.pi)
      cr.move_to(1.0, 0.0)
      cr.arc(0.0, 0.0, 1.0, 0, math.pi)
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

class ProvidedInterfaceShape(xdot.EllipseShape):
    def __init__(self, pen, x0, y0, w, h, objtName, filled=False):
      xdot.EllipseShape.__init__(self,pen,x0,y0,w,h,filled)

    def draw(self, cr, highlight=False,zoom_ratio=-1):
      xdot.EllipseShape.draw(self,cr,highlight,zoom_ratio)

class MisuseCaseShape(xdot.EllipseShape):
    def __init__(self, pen, x0, y0, w, h, filled=False):
      xdot.EllipseShape.__init__(self,pen,x0,y0,w,h,filled)

    def draw(self, cr, highlight=False,zoom_ratio=-1):
      if (zoom_ratio == -1) or (zoom_ratio > HIGH_ZOOM_RATIO):
        xdot.EllipseShape.draw(self,cr,highlight,-1)

   
class RoleShape(xdot.Shape):
    def __init__(self, pen, x0, y0, w, h, filled=False):
        xdot.Shape.__init__(self)
        self.pen = pen.copy()
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h
        self.filled = filled

    def draw(self, cr, highlight=False,zoom_ratio=-1):
      if (zoom_ratio == -1) or (zoom_ratio > HIGH_ZOOM_RATIO):
        cr.save()
        cr.translate(self.x0, self.y0)
        cr.scale(self.w, self.h)

        cr.move_to(-0.5,-0.25)
        cr.rectangle(-0.25,-0.25,0.5,0.75) 
        cr.move_to(0.0,-0.5)
        cr.new_sub_path()
        cr.arc(0.0,-0.5,0.25,0,2.0 * math.pi)
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

class GoalShape(xdot.Shape):
    def __init__(self, pen, x0, y0, w, h, filled=False):
        xdot.Shape.__init__(self)
        self.pen = pen.copy()
        self.x0 = x0
        self.y0 = y0
        self.w = w
        self.h = h
        self.filled = filled

    def draw(self, cr, highlight=False,zoom_ratio=-1):
      if (zoom_ratio == -1) or (zoom_ratio > HIGH_ZOOM_RATIO):
        cr.save()
        cr.translate(self.x0, self.y0)
        cr.scale(self.w, self.h)

        cr.move_to(0.0,-0.5)
        cr.new_sub_path()
        cr.arc(0.0,-0.5,0.5,180 * (math.pi / 180),0 * (math.pi / 180))
        cr.move_to(0.5,0.0)
        cr.new_sub_path()
        cr.arc(0.5,0.0,0.5,270 * (math.pi / 180),90 * (math.pi / 180))
        cr.move_to(0.0,0.5)
        cr.new_sub_path()
        cr.arc(0.0,0.5,0.5,0 * (math.pi / 180),180 * (math.pi / 180))
        cr.move_to(-0.5,0.0)
        cr.new_sub_path()
        cr.arc(-0.5,0.0,0.5,90 * (math.pi / 180),270 * (math.pi / 180))

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


#class RequirementShape(xdot.Shape,ChernoffFace):
#    def __init__(self, pen, x0, y0, w, h,objtName,dp,filled=False):
#        xdot.Shape.__init__(self)
#        ChernoffFace.__init__(self,objtName,dp)
#        self.pen = pen.copy()
#        self.x0 = x0
#        self.y0 = y0
#        self.w = w
#        self.h = h
#        self.filled = filled

#    def draw(self, cr, highlight=False,zoom_ratio=-1):
#      ChernoffFace.draw(self,cr,self.x0,self.y0,self.w,self.h,highlight,zoom_ratio)

class ComponentPolygonShape(xdot.PolygonShape):

    def __init__(self, pen, points, dim, objt,filled=False):
        xdot.PolygonShape.__init__(self,pen,points,filled)

        b = Borg()
        self.dbProxy = b.dbProxy
        self.dim = dim
        self.objt = objt

    def draw(self, cr, highlight=False,zoom_ratio=-1):
      if (zoom_ratio == -1) or (self.dim == 'risk') or (zoom_ratio > LOW_ZOOM_RATIO and (self.dim == 'asset' or self.dim == 'threat' or self.dim == 'vulnerability')) or (zoom_ratio > HIGH_ZOOM_RATIO):
        if (self.dim != 'role'):
          x0, y0 = self.points[-1]
          cr.move_to(x0, y0)
          for x, y in self.points:
            cr.line_to(x, y)
          cr.close_path()
          pen = self.select_pen(highlight)
          if self.filled:
            cr.set_source_rgba(*pen.fillcolor)
            cr.fill_preserve()
            cr.fill()
          else:
            cr.set_dash(pen.dash)
            cr.set_line_width(pen.linewidth)
            cr.set_source_rgba(*pen.color)
            cr.stroke()

        if (len(self.points) == 4):
          if (self.dim != 'role') and ((zoom_ratio == -1) or (zoom_ratio > HIGH_ZOOM_RATIO)):
            if (self.points[0][0] == self.points[1][0]):
              cr.set_source_rgba(*pen.color)
              xs = self.points[0][0]
              ys = self.points[1][1]
              xe = self.points[3][0]
              ye = self.points[2][1]
              cr.move_to(xs,ys + 7.5)
              cr.line_to(xe,ys + 7.5)
              cr.stroke()

        if (zoom_ratio > LOW_ZOOM_RATIO):
          if (self.dim == 'asset'):
            self.decorateAssetNode(cr,zoom_ratio)
          elif (self.dim == 'threat'):
            self.decorateThreatNode(cr,zoom_ratio)
          elif (self.dim == 'vulnerability'):
            self.decorateVulnerabilityNode(cr,zoom_ratio)

        if (zoom_ratio > HIGH_ZOOM_RATIO and self.dim == 'role'):
            self.decorateRoleNode(cr)

    def decorateRoleNode(self,cr):
      xs = self.points[0][0]
      ys = self.points[0][1]
      width = self.points[3][0] - self.points[0][0]
      height = self.points[0][1] - self.points[1][1]
      iconPath = b.iconDir + '/roleNode.png'
      roleSurface = cairo.ImageSurface.create_from_png(iconPath)      
      imageWidth = roleSurface.get_width()
      imageHeight = roleSurface.get_height()
      cr.save()
      cr.set_source_surface(roleSurface,xs + (width/4),ys - height)
      cr.paint()
      cr.restore() 
      

    def decorateAssetNode(self,cr,zoom_ratio):
     if (zoom_ratio == -1) or (zoom_ratio > HIGH_ZOOM_RATIO):
      xs = self.points[0][0]
      ye = self.points[2][1]
      xs = self.points[0][0]
      ys = self.points[1][1]
      xe = self.points[3][0]
      cr.move_to(xs + 30,ye + 7.5)
      cr.line_to(xs + 30,self.points[0][1])
      cr.stroke()

      asset = self.dbProxy.dimensionObject(self.objt,self.dim)
      syProps = asset.securityProperties(self.environment.name(),self.environment.duplicateProperty(),self.environment.overridingEnvironment())
      cx = xs
      cy = ys + 10 
      cr.set_line_width(0.1)
      cr.set_source_rgb(0,0,0)
      cr.rectangle(cx,cy,syProps[0] * 10,3)
      cr.fill()

      ix = xs
      iy = cy + 6 
      cr.set_line_width(0.1)
      cr.set_source_rgb(1,0,0)
      cr.rectangle(ix,iy,syProps[1] * 10,3)
      cr.fill()

      ax = xs
      ay = iy + 6 
      cr.set_line_width(0.1)
      cr.set_source_rgb(0,1,0)
      cr.rectangle(ax,ay,syProps[2] * 10,3)
      cr.fill()

      avx = xs
      avy = ay + 6 
      cr.set_line_width(0.1)
      cr.set_source_rgb(0,0,1)
      cr.rectangle(avx,avy,syProps[3] * 10,3)
      cr.fill()
 
    def decorateThreatNode(self,cr,zoom_ratio):
     if (zoom_ratio > LOW_ZOOM_RATIO) and (zoom_ratio < HIGH_ZOOM_RATIO):
      threat = self.dbProxy.dimensionObject(self.objt,self.dim)
      likelihood = threat.likelihood(self.environment.name(),self.environment.duplicateProperty(),self.environment.overridingEnvironment())
      if (likelihood == 'Incredible'):
        lhoodScore = INCREDIBLE_COLOUR
      elif (likelihood == 'Improbable'):
        lhoodScore = IMPROBABLE_COLOUR
      elif (likelihood == 'Remote'):
        lhoodScore = REMOTE_COLOUR
      elif (likelihood == 'Occasional'):
        lhoodScore = OCCASIONAL_COLOUR
      else:
        lhoodScore = FREQUENT_COLOUR
      x0, y0 = self.points[-1]
      cr.move_to(x0, y0)
      for x, y in self.points:
        cr.line_to(x, y)
      cr.close_path()
      cr.set_source_rgb(lhoodScore[0],lhoodScore[1],lhoodScore[2])
      cr.fill_preserve()
      cr.fill()
     elif (zoom_ratio > HIGH_ZOOM_RATIO):
      xs = self.points[0][0]
      ye = self.points[2][1]
      xs = self.points[0][0]
      ys = self.points[1][1]
      xe = self.points[3][0]
      cr.move_to(xe - 30,ye + 7.5)
      cr.line_to(xe - 30,self.points[0][1])
      cr.stroke()

      threat = self.dbProxy.dimensionObject(self.objt,self.dim)
      syProps = threat.securityProperties(self.environment.name(),self.environment.duplicateProperty(),self.environment.overridingEnvironment())

      lx = xs
      ly = ye + 7.5
      w = xe - xs - 30
      h = self.points[0][1] - (ye + 7.5)
      lhoodScore = (0,0,0)
      likelihood = threat.likelihood(self.environment.name(),self.environment.duplicateProperty(),self.environment.overridingEnvironment())
      if (likelihood == 'Incredible'):
        lhoodScore = INCREDIBLE_COLOUR
      elif (likelihood == 'Improbable'):
        lhoodScore = IMPROBABLE_COLOUR
      elif (likelihood == 'Remote'):
        lhoodScore = REMOTE_COLOUR
      elif (likelihood == 'Occasional'):
        lhoodScore = OCCASIONAL_COLOUR
      else:
        lhoodScore = FREQUENT_COLOUR
      
      cr.set_source_rgb(lhoodScore[0],lhoodScore[1],lhoodScore[2])
      cr.rectangle(lx,ly,w,h)
      cr.fill()

      cLength = syProps[0] * 10
      cx = xe - cLength
      cy = ys + 10 
      cr.set_line_width(0.1)
      cr.set_source_rgb(0,0,0)
      cr.rectangle(cx,cy,cLength,3)
      cr.fill()
      iLength = syProps[1] * 10
      ix = xe - iLength
      iy = cy + 6 
      cr.set_line_width(0.1)
      cr.set_source_rgb(1,0,0)
      cr.rectangle(ix,iy,iLength,3)
      cr.fill()
      avLength = syProps[2] * 10
      avx = xe - avLength
      avy = iy + 6 
      cr.set_line_width(0.1)
      cr.set_source_rgb(0,1,0)
      cr.rectangle(avx,avy,avLength,3)
      cr.fill()
      acLength = syProps[3] * 10
      acx = xe - acLength
      acy = avy + 6 
      cr.set_line_width(0.1)
      cr.set_source_rgb(0,0,1)
      cr.rectangle(acx,acy,acLength,3)
      cr.fill()



    def decorateVulnerabilityNode(self,cr,zoom_ratio):
     if (zoom_ratio > LOW_ZOOM_RATIO) and (zoom_ratio < HIGH_ZOOM_RATIO):
      vulnerability = self.dbProxy.dimensionObject(self.objt,self.dim)
      severity = vulnerability.severity(self.environment.name(),self.environment.duplicateProperty(),self.environment.overridingEnvironment())
      if (severity == 'Negligible'):
        sevCol = NEGLIGIBLE_COLOUR
      elif (severity == 'Marginal'):
        sevCol = MARGINAL_COLOUR
      elif (severity == 'Critical'):
        sevCol = CRITICAL_COLOUR
      else:
        sevCol = CATASTROPHIC_COLOUR
      x0, y0 = self.points[-1]
      cr.move_to(x0, y0)
      for x, y in self.points:
        cr.line_to(x, y)
      cr.close_path()
      cr.set_source_rgb(sevCol[0],sevCol[1],sevCol[2])
      cr.fill_preserve()
      cr.fill()
     elif (zoom_ratio > HIGH_ZOOM_RATIO):
      xs = self.points[0][0]
      ye = self.points[2][1]
      xs = self.points[0][0]
      ys = self.points[1][1]
      xe = self.points[3][0]
      vulnerability = self.dbProxy.dimensionObject(self.objt,self.dim)
      sx = xs
      sy = ye + 7.5
      w = xe - xs
      h = self.points[0][1] - (ye + 7.5)
      sevCol = (0,0,0)
      severity = vulnerability.severity(self.environment.name(),self.environment.duplicateProperty(),self.environment.overridingEnvironment())
      if (severity == 'Negligible'):
        sevCol = NEGLIGIBLE_COLOUR
      elif (severity == 'Marginal'):
        sevCol = MARGINAL_COLOUR
      elif (severity == 'Critical'):
        sevCol = CRITICAL_COLOUR
      else:
        sevCol = CATASTROPHIC_COLOUR
      
      cr.set_source_rgb(sevCol[0],sevCol[1],sevCol[2])
      cr.rectangle(sx,sy,w,h)
      cr.fill()


class XDotAttrParser(xdot.XDotAttrParser):
    def __init__(self, parser, buf,dim='',objt=''):
      xdot.XDotAttrParser.__init__(self,parser,buf)
      self.dim = dim
      self.objt = objt
      b = Borg()
      self.dbProxy = b.dbProxy

    def handle_text(self,x,y,j,w,t):
      self.shapes.append(ComponentTextShape(self.pen, x, y, j, w, t,self.dim))
    
    def handle_ellipse(self, x0, y0, w, h, filled=False):
      if (self.dim == 'required_interface'):
        if filled:
          self.shapes.append(RequiredInterfaceShape(self.pen, x0, y0, w, h,self.objt,filled=True))
        self.shapes.append(RequiredInterfaceShape(self.pen, x0, y0, w, h,self.objt))
        self.shapes.append(InterfaceLabelShape(self.pen, x0, y0 + 13, 0, w * 2,self.objt))
      elif (self.dim == 'provided_interface'):
        if filled:
          self.shapes.append(ProvidedInterfaceShape(self.pen, x0, y0, w, h,self.objt,filled=True))
        self.shapes.append(ProvidedInterfaceShape(self.pen, x0, y0, w, h,self.objt))
        self.shapes.append(InterfaceLabelShape(self.pen, x0, y0 + 13, 0, w * 2,self.objt))
      elif (self.dim == ''):
        if filled:
          self.shapes.append(AttackerShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(AttackerShape(self.pen, x0, y0, w, h))
      elif (self.dim == 'persona'):
        if filled:
          self.shapes.append(PersonaShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(PersonaShape(self.pen, x0, y0, w, h))
      elif (self.dim == 'goal'):
        if filled:
          self.shapes.append(GoalShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(GoalShape(self.pen, x0, y0, w, h))
      elif (self.dim == 'role'):
        if filled:
          self.shapes.append(RoleShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(RoleShape(self.pen, x0, y0, w, h))
      elif (self.dim == 'task'):
        if filled:
          self.shapes.append(TaskShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(TaskShape(self.pen, x0, y0, w, h))
      else:
        if filled:
          self.shapes.append(MisuseCaseShape(self.pen, x0, y0, w, h,filled=True))
        self.shapes.append(MisuseCaseShape(self.pen, x0, y0, w, h))

    def handle_polygon(self,points,filled=False):
      if filled:
        self.shapes.append(ComponentPolygonShape(self.pen,points,self.dim, self.objt,filled=True))
      self.shapes.append(ComponentPolygonShape(self.pen,points,self.dim, self.objt))

class ComponentXDotParser(xdot.XDotParser):

    def __init__(self, xdotcode):
        xdot.XDotParser.__init__(self,xdotcode)
        b = Borg()
        self.dbProxy = b.dbProxy
        
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
                parser = XDotAttrParser(self, attrs[attr],dimObjt[0],dimObjt[1])
                shapes.extend(parser.parse())
        url = attrs.get('URL', None)
        node = xdot.Node(x, y, w, h, shapes, url)
        self.node_by_name[id] = node
        if shapes:
            self.nodes.append(node)



class ComponentDotWidget(xdot.DotWidget):
  def __init__(self):
    xdot.DotWidget.__init__(self)

  def set_xdotcode(self, xdotcode):
    parser = ComponentXDotParser(xdotcode)
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



class ComponentDotWindow(gtk.Window):

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

    def __init__(self,windowTitle,cvName):
        gtk.Window.__init__(self)
        self.graph = xdot.Graph()
        self.theViewName = cvName
        self.traceModel = None
        window = self

        b = Borg()
        self.dbProxy = b.dbProxy

        window.set_title(windowTitle)
        window.set_default_size(512, 512)
        vbox = gtk.VBox()
        window.add(vbox)

        self.widget = ComponentDotWidget()

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
        self.layoutCombo.set_active(1)
        self.layoutHandlerId = self.layoutCombo.connect('changed',self.onLayoutChange)

        self.set_focus(self.widget)

        self.show_all()

    def onLayoutChange(self,action):
      layoutName = self.layoutCombo.get_active_text()
      renderer = 'fdp'
      if (layoutName == 'Hierarchical'):
        renderer = 'dot'
      elif (layoutName == 'Radial'):
        renderer = 'twopi'
      elif (layoutName == 'Circular'):
        renderer = 'circo'

      if (self.traceModel == None):
        interfaces,connectors = self.dbProxy.componentView(self.theViewName)
        self.traceModel = ComponentModel(interfaces,connectors)
      self.set_xdotcode(self.traceModel.layout(renderer))

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
      try:
        proxy = self.dbProxy
        
        self.traceModel = ComponentModel(b.dbProxy.componentView(self.theViewName))
        self.set_xdotcode(self.traceModel.graph())
        self.widget.zoom_to_fit()

      except ARMException, ex:
        dlg = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,message_format=str(ex),buttons=gtk.BUTTONS_OK)
        dlg.set_title('Component Model Viewer')
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
