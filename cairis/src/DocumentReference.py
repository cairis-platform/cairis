#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DocumentReference.py $ $Id: DocumentReference.py 409 2011-01-14 20:22:34Z shaf $

class DocumentReference:
  def __init__(self,refId,refName,docName,cName,docExc):
    self.theId = refId
    self.theName = refName
    self.theDocName = docName
    self.theContributor = cName
    self.theExcerpt = docExc

  def id(self): return self.theId
  def name(self): return self.theName
  def contributor(self): return self.theContributor
  def document(self): return self.theDocName
  def excerpt(self): return self.theExcerpt
