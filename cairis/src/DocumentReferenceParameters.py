#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DocumentReferenceParameters.py $ $Id: DocumentReferenceParameters.py 409 2011-01-14 20:22:34Z shaf $
from ObjectCreationParameters import ObjectCreationParameters

class DocumentReferenceParameters(ObjectCreationParameters):
  def __init__(self,refName,docName,cName,docExc):
    ObjectCreationParameters.__init__(self)
    self.theName = refName
    self.theDocName = docName
    self.theContributor = cName
    self.theExcerpt = docExc

  def name(self): return self.theName
  def document(self): return self.theDocName
  def contributor(self): return self.theContributor
  def description(self): return self.theExcerpt
