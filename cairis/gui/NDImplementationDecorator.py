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


import gtk
import os

__author__ = 'Shamal Faily'

class NDImplementationDecorator:
  def __init__(self,builder):
    self.theBuilder = builder

  def updateTextCtrl(self,ctrlName,ctrlTxt):
    ctrl = self.theBuilder.get_object(ctrlName)
    ctrl.set_text(ctrlTxt)

  def updateCheckCtrl(self,ctrlName,ctrlFlag):
    ctrl = self.theBuilder.get_object(ctrlName)
    ctrl.set_active(ctrlFlag)

  def updateImageCtrl(self,ctrlName,imageFile):
    if ((imageFile == None) or (imageFile == '') or (os.path.exists(imageFile) == False)):
      return
    else:
      ctrl = self.theBuilder.get_object(ctrlName)
      ctrl.set_from_file(imageFile)


  def updateMLTextCtrl(self,ctrlName,ctrlTxt):
    ctrl = self.theBuilder.get_object(ctrlName)
    buf = gtk.TextBuffer()
    buf.set_text(ctrlTxt)
    ctrl.set_buffer(buf)

  def updateListCtrl(self,ctrlName,labels,model,values):
    ctrl = self.theBuilder.get_object(ctrlName)
    for idx,label in enumerate(labels):
      renderer = gtk.CellRendererText()
      col = gtk.TreeViewColumn(label)
      col.set_resizable(True)
      ctrl.append_column(col)
      col.pack_start(renderer,True)
      col.set_attributes(renderer,text=idx)
    ctrl.set_model(model)
    for value in values:
      model.append(value)

  def updateComboCtrl(self,ctrlName,labels,value):
    ctrl = self.theBuilder.get_object(ctrlName)
    model = gtk.ListStore(str)
    renderer = gtk.CellRendererText()
    ctrl.pack_start(renderer, True)
    ctrl.add_attribute(renderer,'text',0)
    ctrl.set_model(model)
    selIdx = 0
    for idx,v in enumerate(labels):
      if (v == value):
        selIdx = idx
      model.append([v])
    ctrl.set_active(selIdx)

  def updateButtonLabel(self,ctrlName,newLabel):
    ctrl = self.theBuilder.get_object(ctrlName)
    ctrl.set_label(newLabel)

  def getText(self,ctrlName):
    ctrl = self.theBuilder.get_object(ctrlName)
    return ctrl.get_text()

  def getMLText(self,ctrlName): 
    ctrl = self.theBuilder.get_object(ctrlName)
    buf = ctrl.get_buffer()
    return buf.get_text(buf.get_start_iter(),buf.get_end_iter())

  def getComboValue(self,ctrlName):
    ctrl = self.theBuilder.get_object(ctrlName)
    return ctrl.get_active_text()
