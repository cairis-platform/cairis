#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DomainPropertyParameters.py $ $Id: DomainPropertyParameters.py 511 2011-10-30 15:48:53Z shaf $
from ObjectCreationParameters import ObjectCreationParameters

class DomainPropertyParameters(ObjectCreationParameters):
  def __init__(self,name,desc,dpType,dpOrig):
    ObjectCreationParameters.__init__(self)
    self.theName = name
    self.theDescription = desc
    self.theType = dpType
    self.theOriginator = dpOrig

  def name(self): return self.theName
  def description(self): return self.theDescription
  def type(self): return self.theType
  def originator(self): return self.theOriginator
