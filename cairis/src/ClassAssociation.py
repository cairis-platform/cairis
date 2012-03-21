#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ClassAssociation.py $ $Id: ClassAssociation.py 439 2011-03-19 22:01:02Z shaf $
class ClassAssociation:
  def __init__(self,associationId,envName,headName,headDim,headNav,headType,headMultiplicity,headRole,tailRole,tailMultiplicity,tailType,tailNav,tailDim,tailName,rationale=''):
    self.theId = associationId
    self.theEnvironmentName = envName
    self.theHeadAsset = headName
    self.theHeadType = headType
    self.theHeadDim = headDim
    self.theHeadNavigation = headNav
    self.theHeadMultiplicity = headMultiplicity
    self.theHeadRole = headRole
    self.theTailRole = tailRole
    self.theTailMultiplicity = tailMultiplicity
    self.theTailType = tailType
    self.theTailNavigation = tailNav
    self.theTailDim = tailDim
    self.theTailAsset = tailName
    self.theRationale = rationale

  def id(self): return self.theId
  def environment(self): return self.theEnvironmentName
  def headAsset(self): return self.theHeadAsset
  def headDimension(self): return self.theHeadDim
  def headNavigation(self): return self.theHeadNavigation
  def headType(self): return self.theHeadType
  def headMultiplicity(self): return self.theHeadMultiplicity
  def headRole(self): return self.theHeadRole
  def tailRole(self): return self.theTailRole
  def tailMultiplicity(self): return self.theTailMultiplicity
  def tailType(self): return self.theTailType
  def tailNavigation(self): return self.theTailNavigation
  def tailDimension(self): return self.theTailDim
  def tailAsset(self): return self.theTailAsset
  def rationale(self): return self.theRationale
