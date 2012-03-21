#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ConceptReferenceParameters.py $ $Id: ConceptReferenceParameters.py 330 2010-10-31 15:01:28Z shaf $
from ObjectCreationParameters import ObjectCreationParameters

class ConceptReferenceParameters(ObjectCreationParameters):
  def __init__(self,refName,dimName,objtName,cDesc):
    ObjectCreationParameters.__init__(self)
    self.theName = refName
    self.theDimName = dimName
    self.theObjtName = objtName
    self.theDescription = cDesc

  def name(self): return self.theName
  def dimension(self): return self.theDimName
  def objectName(self): return self.theObjtName
  def description(self): return self.theDescription
