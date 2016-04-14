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
from DocumentReferenceNodeDialog import DocumentReferenceNodeDialog
from ConceptReferenceNodeDialog import ConceptReferenceNodeDialog

from Borg import Borg

def build(url,isApModel = True):
  dim,objtName = url.split('#')
  b = Borg()
  proxy = b.dbProxy
  builder = gtk.Builder()
  
  gladeFile = './config/imvnodes/imvnodes.xml'
  builder.add_from_file(gladeFile)

  
  dlg = 0
  if (dim == 'grounds'):
    groundsFn = proxy.getGrounds
    if (isApModel == False):
      groundsFn = proxy.getTaskGrounds
    dimName,refName,refDesc = groundsFn(objtName)
    
    if (dimName == 'document'):
      dlg = DocumentReferenceNodeDialog(objtName,refName,refDesc,builder)
    else:
      dlg = ConceptReferenceNodeDialog(objtName,dimName,refName,refDesc,builder)
  elif (dim == 'warrant'):
    warrantFn = proxy.getWarrant
    if (isApModel == False):
      warrantFn = proxy.getTaskWarrant
    dimName,refName,refDesc = warrantFn(objtName)
    if (dimName == 'document'):
      dlg = DocumentReferenceNodeDialog(objtName,refName,refDesc,builder)
    else:
      dlg = ConceptReferenceNodeDialog(objtName,dimName,refName,refDesc,builder)
  elif (dim == 'rebuttal'):
    rebuttalFn = proxy.getRebuttal
    if (isApModel == False):
      rebuttalFn = proxy.getTaskRebuttal
    dimName,refName,refDesc = rebuttalFn(objtName)
    if (dimName == 'document'):
      dlg = DocumentReferenceNodeDialog(objtName,refName,refDesc,builder)
    else:
      dlg = ConceptReferenceNodeDialog(objtName,dimName,refName,refDesc,builder)
  else:
    return 
  dlg.show()
  builder.connect_signals(dlg)
