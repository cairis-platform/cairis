#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DocumentReferenceNodeDialog.py $ $Id: DocumentReferenceNodeDialog.py 263 2010-06-20 15:53:44Z shaf $

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
