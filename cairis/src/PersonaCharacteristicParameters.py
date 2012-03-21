#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaCharacteristicParameters.py $ $Id: PersonaCharacteristicParameters.py 285 2010-07-01 21:32:07Z shaf $
from ObjectCreationParameters import ObjectCreationParameters

class PersonaCharacteristicParameters(ObjectCreationParameters):
  def __init__(self,pName,modQual,vName,cDesc,pcGrounds,pcWarrant,pcBacking,pcRebuttal):
    ObjectCreationParameters.__init__(self)
    self.thePersonaName = pName
    self.theModQual = modQual
    self.theVariable = vName
    self.theCharacteristic = cDesc
    self.theGrounds = pcGrounds
    self.theWarrant = pcWarrant
    self.theBacking = pcBacking
    self.theRebuttal = pcRebuttal

  def persona(self): return self.thePersonaName
  def qualifier(self): return self.theModQual
  def behaviouralVariable(self): return self.theVariable
  def characteristic(self): return self.theCharacteristic
  def grounds(self): return self.theGrounds
  def warrant(self): return self.theWarrant
  def backing(self): return self.theBacking
  def rebuttal(self): return self.theRebuttal
