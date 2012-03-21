#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ConceptReference.py $ $Id: ConceptReference.py 330 2010-10-31 15:01:28Z shaf $

class ConceptReference:
  def __init__(self,refId,refName,dimName,objtName,cDesc):
    self.theId = refId
    self.theName = refName
    self.theDimName = dimName
    self.theObjtName = objtName
    self.theDescription = cDesc

  def id(self): return self.theId
  def name(self): return self.theName
  def dimension(self): return self.theDimName
  def objectName(self): return self.theObjtName
  def description(self): return self.theDescription
