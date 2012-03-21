#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TraceDialogParameters.py $ $Id: TraceDialogParameters.py 249 2010-05-30 17:07:31Z shaf $
import DialogClassParameters

class TraceDialogParameters(DialogClassParameters.DialogClassParameters):
  def __init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag,fromObjt,fromId,toObjt,toId):
    DialogClassParameters.DialogClassParameters.__init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag)
    self.theOldFromObject = fromObjt
    self.theOldFromId = fromId
    self.theOldToObject = toObjt
    self.theOldToId = toId

  def fromObject(self): return self.theOldFromObject
  def fromId(self): return self.theOldFromId
  def toObject(self): return self.theOldToObject
  def toId(self): return self.theOldToId
