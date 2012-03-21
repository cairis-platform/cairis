#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TaskDialogParameters.py $ $Id: TaskDialogParameters.py 249 2010-05-30 17:07:31Z shaf $
import DialogClassParameters

class TaskDialogParameters(DialogClassParameters.DialogClassParameters):
  def __init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag,dp):
    DialogClassParameters.DialogClassParameters.__init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag)
    self.theProxy = dp

  def proxy(self): return self.theProxy
