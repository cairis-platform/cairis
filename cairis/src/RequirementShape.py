import xdot
from ChernoffFace import ChernoffFace


class RequirementShape(xdot.Shape,ChernoffFace):
  def __init__(self, pen, x0, y0, w, h,objtName,dp,filled=False):
    xdot.Shape.__init__(self)
    ChernoffFace.__init__(self,objtName,dp)
    self.pen = pen.copy()
    self.x0 = x0
    self.y0 = y0
    self.w = w
    self.h = h
    self.filled = filled

  def draw(self, cr, highlight=False,zoom_ratio=-1):
    ChernoffFace.draw(self,cr,self.x0,self.y0,self.w,self.h,highlight,zoom_ratio)
