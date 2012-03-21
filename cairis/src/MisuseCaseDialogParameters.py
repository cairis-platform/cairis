#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MisuseCaseDialogParameters.py $ $Id: MisuseCaseDialogParameters.py 249 2010-05-30 17:07:31Z shaf $
import ScenarioDialogParameters

class ScenarioDialogParameters(ScenarioDialogParameters.ScenarioDialogParameters):
  def __init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag,dp):
    ScenarioDialogParameters.ScenarioDialogParameters.__init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag,dp)

  def proxy(self): return self.theProxy
