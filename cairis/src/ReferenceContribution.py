class ReferenceContribution:
  def __init__(self,src,dest,me,cont):
    self.theSource = src
    self.theDestination = dest
    self.theMeansEnd = me
    self.theContribution = cont

  def source(self): return self.theSource
  def destination(self): return self.theDestination
  def meansEnd(self): return self.theMeansEnd
  def contribution(self): return self.theContribution
