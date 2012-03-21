#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Target.py $ $Id: Target.py 551 2012-02-03 20:18:59Z shaf $
class Target:
  def __init__(self,tName,tEffectiveness,tRat):
    self.theName = tName
    self.theEffectiveness = tEffectiveness
    self.theRationale = tRat

  def name(self): return self.theName
  def effectiveness(self): return self.theEffectiveness
  def rationale(self): return self.theRationale
 
  def __getitem__(self,idx): 
    if (idx == 0): 
      return self.theName
    elif (idx == 1):
      return self.theEffectiveness
    else:
      return self.theRationale
