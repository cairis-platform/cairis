#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DomainProperty.py $ $Id: DomainProperty.py 511 2011-10-30 15:48:53Z shaf $
class DomainProperty:
  def __init__(self,dpId,dpName,dpDesc,dpType,dpOrig):
    self.theId = dpId
    self.theName = dpName
    self.theDescription = dpDesc
    self.theType = dpType
    self.theOriginator = dpOrig

  def id(self): return self.theId
  def name(self): return self.theName
  def description(self): return self.theDescription
  def type(self): return self.theType
  def originator(self): return self.theOriginator
