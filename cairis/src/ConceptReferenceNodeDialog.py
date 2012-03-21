#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ConceptReferenceNodeDialog.py $ $Id: ConceptReferenceNodeDialog.py 330 2010-10-31 15:01:28Z shaf $

import sys
import gtk
import gobject
from NDImplementationDecorator import NDImplementationDecorator


class ConceptReferenceNodeDialog:
  def __init__(self,refName,dimName,objtName,refDesc,builder):
    self.window = builder.get_object("ConceptReferenceNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("conceptReferenceNameCtrl",refName)
    self.decorator.updateTextCtrl("conceptReferenceTypeCtrl",dimName)
    self.decorator.updateTextCtrl("conceptReferenceArtifactCtrl",objtName)
    self.decorator.updateMLTextCtrl("conceptReferenceDescriptionCtrl",refDesc)

    self.window.resize(350,200)

  def on_conceptReferenceOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
