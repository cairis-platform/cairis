#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DotTrace.py $ $Id: DotTrace.py 249 2010-05-30 17:07:31Z shaf $
import Trace

class DotTrace(Trace.Trace):
  def __init__(self,fObjt,fName,tObjt,tName):
    Trace.Trace.__init__(self,fObjt,fName,tObjt,tName)
