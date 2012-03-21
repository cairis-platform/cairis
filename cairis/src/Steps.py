from Step import Step

class Steps:
  def __init__(self):
    self.theSteps = []

  def __getitem__(self,stepNo):
    return self.theSteps[stepNo]

  def __setitem__(self,stepNo,s):
    self.theSteps[stepNo] = s

  def size(self):
    return len(self.theSteps)

  def append(self,s):
    self.theSteps.append(s)

  def remove(self,stepNo):
    self.theSteps.pop(stepNo)

  def insert(self,pos,s):
    self.theSteps.insert(pos,s)
