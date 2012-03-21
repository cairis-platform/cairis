#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ClassAssociationParameters.py $ $Id: ClassAssociationParameters.py 439 2011-03-19 22:01:02Z shaf $
import ObjectCreationParameters

class ClassAssociationParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,envName,headName,headDim,headNav,headType,headMultiplicity,headRole,tailRole,tailMultiplicity,tailType,tailNav,tailDim,tailName,rationale = ''):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theEnvironmentName = envName
    self.theHeadAsset = headName
    self.theHeadDim = headDim
    self.theHeadNav = headNav
    self.theHeadType = headType
    self.theHeadMultiplicity = headMultiplicity
    self.theHeadRole = headRole
    self.theTailRole = tailRole
    self.theTailMultiplicity = tailMultiplicity
    self.theTailType = tailType
    self.theTailNav = tailNav
    self.theTailDim = tailDim
    self.theTailAsset = tailName
    self.theRationale = rationale

  def environment(self): return self.theEnvironmentName
  def headAsset(self): return self.theHeadAsset
  def headDimension(self): return self.theHeadDim
  def headNavigation(self): return self.theHeadNav
  def headType(self): return self.theHeadType
  def headMultiplicity(self): return self.theHeadMultiplicity
  def headRole(self): return self.theHeadRole
  def tailRole(self): return self.theTailRole
  def tailMultiplicity(self): return self.theTailMultiplicity
  def tailType(self): return self.theTailType
  def tailNavigation(self): return self.theTailNav
  def tailDimension(self): return self.theTailDim
  def tailAsset(self): return self.theTailAsset
  def rationale(self): return self.theRationale
