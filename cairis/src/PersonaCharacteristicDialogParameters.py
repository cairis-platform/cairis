#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/PersonaCharacteristicDialogParameters.py $ $Id: PersonaCharacteristicDialogParameters.py 249 2010-05-30 17:07:31Z shaf $
import DialogClassParameters

class PersonaCharacteristicDialogParameters(DialogClassParameters.DialogClassParameters):
  def __init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag,pName,bvName):
    DialogClassParameters.DialogClassParameters.__init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag)
    self.thePersonaName = pName
    self.theBehaviouralVariable = bvName

  def persona(self): return self.thePersonaName
  def behaviouralVariable(self): return self.theBehaviouralVariable
