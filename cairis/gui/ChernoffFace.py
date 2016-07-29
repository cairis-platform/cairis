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


import random, math
from math import pi
from cairis.core.MySQLDatabaseProxy import MySQLDatabaseProxy
from cairis.core.Requirement import Requirement
import cairis.core.RequirementScoreFactory

__author__ = 'Shamal Faily'

class ChernoffFace:
  def __init__(self,objtName,dp):
    self.p = cairis.core.RequirementScoreFactory.build(dp.dimensionObject(objtName,'requirement'))
    self.head_radius = 30
    self.eye_radius = 5
    self.eye_left_x = 40
    self.eye_right_x = 60
    self.eye_y = 40
    self.pupil_radius = 1.5
    self.eyebrow_l_l_x = 35
    self.eyebrow_r_l_x = 55
    self.eyebrow_l_r_x = 45
    self.eyebrow_r_r_x = 65
    self.eyebrow_y = 30
    self.nose_apex_x = 50
    self.nose_apex_y = 45
    self.nose_height = 16
    self.nose_width = 8
    self.mouth_y = 65


  def draw(self, cr, x=0, y=0, width=100, height=100,highlight=False,zoom_ratio=-1):
   reqScore = self.p[0] + self.p[1] + self.p[2]
   if (zoom_ratio == -1) or (zoom_ratio < 0.4 and reqScore < 2) or (zoom_ratio > 0.4):
    self.cr = cr
    self.head_radius = 18
    self.eye_radius = 2.5
    self.eye_left_x = x - 5
    self.eye_right_x = x + 5
    self.eye_y = y - 5
    self.eyebrow_l_l_x = self.eye_left_x - 2.5
    self.eyebrow_r_l_x = self.eye_right_x - 2.5
    self.eyebrow_l_r_x = self.eye_left_x + 2.5
    self.eyebrow_r_r_x = self.eye_right_x + 2.5
    self.eyebrow_y = self.eye_y - 5
    self.nose_apex_x = x
    self.nose_apex_y = y - 3
    self.nose_height = 2
    self.nose_width = 1.5
    self.mouth_y = y + 7

    self.x_factor = width / 100.0
    self.y_factor = height / 100.0
    self.x_origin = x
    self.y_origin = y

    self.cr.new_sub_path()
    self.xOval(x,y, self.head_radius, self.head_radius)



    eye_spacing = int((0.5 - 0.5) * 10)
    eye_size = int( ((0.5 - 0.5) / 2.0) * 10 )
    e0, e1 = self.eccentricities(self.p[1])

    self.cr.new_sub_path()
    self.xOval(self.eye_left_x - eye_spacing, self.eye_y,
               self.eye_radius + eye_size + e0, self.eye_radius + eye_size + e1)
    self.cr.new_sub_path()
    self.xOval(self.eye_right_x + eye_spacing, self.eye_y,
               self.eye_radius + eye_size + e0, self.eye_radius + eye_size + e1)

    pupil_size_x = int(max(1, self.p[1] * self.pupil_radius * self.x_factor))
    pupil_size_y = int(max(1, self.p[1] * self.pupil_radius * self.y_factor))
    self.cr.new_sub_path()
    self.xFillOval(self.eye_left_x, self.eye_y,
                   pupil_size_x, pupil_size_y)
    self.cr.new_sub_path()
    self.xFillOval(self.eye_right_x, self.eye_y,
                   pupil_size_x, pupil_size_y)

    y1 = self.eyebrow_y + int((self.p[0] - 0.5) * 10)
    y2 = self.eyebrow_y - int((self.p[0] - 0.5) * 10)

    self.xLine(self.eyebrow_l_l_x, y1, self.eyebrow_l_r_x, y2)
    self.xLine(self.eyebrow_r_l_x, y2, self.eyebrow_r_r_x, y1)

    y += int(((0.5 - 0.5) / 2.0) * 10)
    self.cr.save()
    self.cr.move_to(self.nose_apex_x, self.nose_apex_y)
    self.cr.line_to(self.nose_apex_x - (self.nose_width / 2), y)
    self.cr.line_to(self.nose_apex_x + (self.nose_width / 2), y)
    self.cr.close_path()
    self.cr.restore()

    mouth_size = ((0.5 - 0.5) * 10)
    x1 = self.eye_left_x - mouth_size
    y1 = self.mouth_y
    x2 = self.eye_right_x + mouth_size
    y2 = self.mouth_y
    x3 = ((x2 - x1) / 2) + x1
    y3 = ((self.p[2] - 0.5) * 10) + self.mouth_y
    self.draw_lip(x1, y1, x2, y2, x3, y3)

    pen = self.select_pen(highlight)
    self.cr.set_line_width(pen.linewidth)
    self.cr.set_source_rgba(*pen.color) 
    self.cr.stroke()

  def draw_lip(self, x1, y1, x2, y2, x3, y3):
    x1_2 = x1 ** 2
    x2_2 = x2 ** 2
    x3_2 = x3 ** 2
    denom = (x1_2 * (x2 - x3)) \
             + (x1 * (x3_2 - x2_2)) \
             + (x2_2 * x3) \
             - (x3_2 * x2)
    denom = float(denom)

    a = ( (y1 * (x2 - x3))
           + (x1 * (y3 - y2))
           + (y2 * x3)
           + -(y3 * x2)
        ) / denom

    bb = ( (x1_2 * (y2 - y3))
            + (y1 * (x3_2 - x2_2))
            + (x2_2 * y3)
            - (x3_2 * y2)
         ) / denom

    c = ( (x1_2 * ((x2 * y3) - (x3 * y2)))
           + (x1 * ((x3_2 * y2) - (x2_2 * y3)))
           + (y1 * ((x2_2 * x3) - (x3_2 * x2)))
        ) / denom

    last_x = int(x1)
    last_y = int(y1)
    for i in xrange(int(x1), int(x2+1)):
      new_x = i
      new_y = int(a * i**2 + bb*i + c)
      self.xLine(last_x, last_y, new_x, new_y)
      last_x = new_x
      last_y = new_y


  def eccentricities(self, p):
    if p > 0.5:
      return [int((p - 0.5) * 20.0), 0]
    else:
      return [0, int(abs(p - 0.5) * 20.0)]

  def xOval(self,x,y,height_r,width_r):
    self.cr.save()
    self.cr.translate(x,y)
    self.cr.scale(width_r, height_r)
    self.cr.arc(0.0,0.0,1.0,0.0,2.0 * pi)
    self.cr.restore()

  def xFillOval(self,x,y,height_r,width_r):
    self.cr.save()
    self.cr.translate(x,y)
    self.cr.scale(width_r, height_r)
    self.cr.arc(0.0,0.0,1.0,0.0,2.0 * pi)
    self.cr.restore()

  def xLine(self,x1,y1,x2,y2):
    self.cr.save()
    self.cr.move_to(x1,y1)
    self.cr.line_to(x2,y2)
    self.cr.restore()
