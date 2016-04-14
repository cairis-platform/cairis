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
import gtk.glade
import os
from DomainNodeDialog import DomainNodeDialog

from Borg import Borg

def build(url):
  dim,objtName = url.split('#')
  if (dim == 'domain' or dim == 'designeddomain'):
    b = Borg()
    proxy = b.dbProxy
    builder = gtk.Builder()
    gladeFile = './config/imvnodes/imvnodes.xml'
    builder.add_from_file(gladeFile)
    objt = proxy.dimensionObject(objtName,'domain')
    dlg = DomainNodeDialog(objt,builder)
    dlg.show()
    builder.connect_signals(dlg)
