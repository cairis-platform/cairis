#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TraceParameters.py $ $Id: TraceParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class TraceParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,fromObjt,fromName,toObjt,toName):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theFromObject = fromObjt
    self.theFromName = fromName
    self.theToObject = toObjt
    self.theToName = toName

  def fromObject(self): return self.theFromObject
  def fromName(self): return self.theFromName
  def toObject(self): return self.theToObject
  def toName(self): return self.theToName
