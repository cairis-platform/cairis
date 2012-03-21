#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AssumptionNodeDialogFactory.py $ $Id: AssumptionNodeDialogFactory.py 396 2011-01-06 15:18:19Z shaf $

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
  
  gladeFile = os.environ['IRIS_CONFIG'] + '/imvnodes/imvnodes.xml'
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
