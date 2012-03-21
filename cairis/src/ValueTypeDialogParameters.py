#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ValueTypeDialogParameters.py $ $Id: ValueTypeDialogParameters.py 427 2011-02-27 12:29:59Z shaf $
import DialogClassParameters

class ValueTypeDialogParameters(DialogClassParameters.DialogClassParameters):
  def __init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag,vType,envName = ''):
    DialogClassParameters.DialogClassParameters.__init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag)
    self.theType = vType
    self.theEnvironmentName = envName

  def type(self): return self.theType
  def environment(self): return self.theEnvironmentName
