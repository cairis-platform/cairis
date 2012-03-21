#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ResponseDialogParameters.py $ $Id: ResponseDialogParameters.py 415 2011-01-21 14:59:08Z shaf $
import DialogClassParameters

class ResponseDialogParameters(DialogClassParameters.DialogClassParameters):
  def __init__(self,winId,winLabel,dClass = None,createId = -1,setterFn = None,creationFlag = False,respPanel = None,respType = ''):
    DialogClassParameters.DialogClassParameters.__init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag)
    self.theResponsePanel = respPanel
    self.theResponseType = respType

  def panel(self): return self.theResponsePanel
  def responseType(self): return self.theResponseType
