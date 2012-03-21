#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaCharacteristicDialogParameters.py $ $Id: PersonaCharacteristicDialogParameters.py 249 2010-05-30 17:07:31Z shaf $
import DialogClassParameters

class TaskCharacteristicDialogParameters(DialogClassParameters.DialogClassParameters):
  def __init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag,tName,showTaskCombo = True):
    DialogClassParameters.DialogClassParameters.__init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag)
    self.theTaskName = tName
    self.taskComboShown = showTaskCombo

  def task(self): return self.theTaskName
  def showTask(self): return self.taskComboShown
