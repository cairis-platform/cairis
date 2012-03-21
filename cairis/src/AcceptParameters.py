#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AcceptParameters.py $ $Id: AcceptParameters.py 330 2010-10-31 15:01:28Z shaf $
import ObjectCreationParameters

class ResponseParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,respName,respRisk):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = respName
    self.theRisk = respRisk

  def name(self): return self.theName
  def risk(self): return self.theRisk
