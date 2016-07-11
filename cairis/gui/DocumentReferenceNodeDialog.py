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


import sys
import gtk
import gobject
from NDImplementationDecorator import NDImplementationDecorator


class DocumentReferenceNodeDialog:
  def __init__(self,refName,docName,docExc,builder):
    self.window = builder.get_object("DocumentReferenceNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("documentReferenceNameCtrl",refName)
    self.decorator.updateTextCtrl("documentReferenceDocumentCtrl",docName)
    self.decorator.updateMLTextCtrl("documentReferenceExcerptCtrl",docExc)

    self.window.resize(350,200)

  def on_documentReferenceOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
