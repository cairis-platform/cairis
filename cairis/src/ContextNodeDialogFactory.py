#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ContextNodeDialogFactory.py $ $Id: ContextNodeDialogFactory.py 249 2010-05-30 17:07:31Z shaf $
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
    gladeFile = os.environ['IRIS_CONFIG'] + '/imvnodes/imvnodes.xml'
    builder.add_from_file(gladeFile)
    objt = proxy.dimensionObject(objtName,'domain')
    dlg = DomainNodeDialog(objt,builder)
    dlg.show()
    builder.connect_signals(dlg)
