#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaCharacteristic.py $ $Id: PersonaCharacteristic.py 285 2010-07-01 21:32:07Z shaf $

class PersonaCharacteristic:
  def __init__(self,pcId,pName,modQual,vName,cDesc,pcGrounds,pcWarrant,pcBacking,pcRebuttal):
    self.theId = pcId
    self.thePersonaName = pName
    self.theModQual = modQual
    self.theVariable = vName
    self.theCharacteristic = cDesc
    self.theGrounds = pcGrounds
    self.theWarrant = pcWarrant
    self.theBacking = pcBacking
    self.theRebuttal = pcRebuttal
       

  def id(self): return self.theId
  def persona(self): return self.thePersonaName
  def qualifier(self): return self.theModQual
  def behaviouralVariable(self): return self.theVariable
  def characteristic(self): return self.theCharacteristic
  def grounds(self): return self.theGrounds
  def warrant(self): return self.theWarrant
  def backing(self): return self.theBacking
  def rebuttal(self): return self.theRebuttal
