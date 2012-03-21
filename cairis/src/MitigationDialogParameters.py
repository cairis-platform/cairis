#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MitigationDialogParameters.py $ $Id: MitigationDialogParameters.py 249 2010-05-30 17:07:31Z shaf $
import DialogClassParameters

class MitigationDialogParameters(DialogClassParameters.DialogClassParameters):
  def __init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag,types,costs):
    DialogClassParameters.DialogClassParameters.__init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag)
    self.theTypes = types
    self.theCosts = costs

  def types(self): return self.theTypes
  def costs(self): return self.theCosts
