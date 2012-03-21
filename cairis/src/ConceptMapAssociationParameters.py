#$URL$ $Id$
import ObjectCreationParameters

class ConceptMapAssociationParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,fromName,toName,lbl,fromEnv,toEnv):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theFromName = fromName
    self.theToName = toName
    self.theLabel = lbl
    self.theFromEnvironmentName = fromEnv
    self.theToEnvironmentName = toEnv

  def fromEnvironment(self): return self.theFromEnvironmentName
  def toEnvironment(self): return self.theToEnvironmentName
  def fromName(self): return self.theFromName
  def toName(self): return self.theToName
  def label(self): return self.theLabel
