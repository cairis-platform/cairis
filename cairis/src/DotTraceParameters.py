#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DotTraceParameters.py $ $Id: DotTraceParameters.py 249 2010-05-30 17:07:31Z shaf $
import TraceParameters

class DotTraceParameters(TraceParameters.TraceParameters):
  def __init__(self,fromObjt,fromName,toObjt,toName):
    TraceParameters.TraceParameters.__init__(self,fromObjt,fromName,toObjt,toName)
