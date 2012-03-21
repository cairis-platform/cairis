#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Responsibility.py $ $Id: Responsibility.py 249 2010-05-30 17:07:31Z shaf $
class Responsibility:
  def __init__(self,respId,respName):
    self.theId = respId
    self.theName = respName

  def id(self): return self.theId
  def name(self): return self.theName
