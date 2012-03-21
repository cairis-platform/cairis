class Step:
  def __init__(self,stepTxt = '',stepSyn = '',stepActor = '',stepActorType = ''):
    self.theExceptions = {}
    self.theStepText = stepTxt
    self.theSynopsis = stepSyn
    self.theActor = stepActor
    self.theActorType = stepActorType

  def synopsis(self): return self.theSynopsis

  def actor(self): return self.theActor

  def actorType(self): return self.theActorType

  def setSynopsis(self,s): self.theSynopsis = s

  def setActor(self,a): self.theActor = a

  def setActorType(self,at): self.theActorType = at

  def __str__(self):
    return self.theStepText

  def addException(self,exc):
    self.theExceptions[exc[0]] = exc

  def deleteException(self,excName):
    del self.theExceptions[excName]
    
  def text(self):
    return self.theStepText

  def setText(self,txt):
    self.theStepText = txt

  def exceptions(self):
    if len(self.theExceptions) > 0:
      return self.theExceptions.keys()
    else:
      return []

  def exception(self,excName):
    return self.theExceptions[excName]

  def setException(self,oldExcName,exc):
    del self.theExceptions[oldExcName] 
    self.theExceptions[exc[0]] = exc
