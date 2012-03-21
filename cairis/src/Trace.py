#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Trace.py $ $Id: Trace.py 249 2010-05-30 17:07:31Z shaf $
class Trace:
  def __init__(self,fObjt,fName,tObjt,tName):
    self.theFromObject = fObjt
    self.theFromName = fName
    self.theToObject = tObjt
    self.theToName = tName

  def fromObject(self): return self.theFromObject
  def fromName(self): return self.theFromName
  def toObject(self): return self.theToObject
  def toName(self): return self.theToName
