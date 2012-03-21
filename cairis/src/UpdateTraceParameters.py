#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/UpdateTraceParameters.py $ $Id: UpdateTraceParameters.py 249 2010-05-30 17:07:31Z shaf $
import TraceParameters

class UpdateTraceParameters(TraceParameters.TraceParameters):
  def __init__(self,fromObjt,fromId,toObjt,toId,fromName,toName,oldFromId,oldToId):
    TraceParameters.TraceParameters.__init__(self,fromObjt,fromId,toObjt,toId,fromName,toName)
    self.theOriginalFromId = oldFromId
    self.theOriginalToId = oldToId

  def oldFromId(self): return self.theOriginalFromId
  def oldToId(self): return self.theOriginalToId
