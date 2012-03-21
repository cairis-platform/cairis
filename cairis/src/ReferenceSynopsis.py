class ReferenceSynopsis:
  def __init__(self,rsId,refName,synName,dimName,aType,aName):
    self.theId = rsId
    self.theReference = refName
    self.theSynopsis = synName
    self.theDimension = dimName
    self.theActorType = aType
    self.theActor = aName

  def id(self): return self.theId
  def reference(self): return self.theReference
  def synopsis(self): return self.theSynopsis
  def dimension(self): return self.theDimension
  def actorType(self): return self.theActorType
  def actor(self): return self.theActor 
