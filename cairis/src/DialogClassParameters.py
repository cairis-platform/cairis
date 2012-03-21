#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DialogClassParameters.py $ $Id: DialogClassParameters.py 413 2011-01-20 14:49:30Z shaf $

class DialogClassParameters:
  def __init__(self,winId,winLabel,dClass = None,createId = -1,setterFn = None,creationFlag = False):
    self.theWinId = winId
    self.theWinLabel = winLabel
    self.theDialogClass = dClass 
    self.theCreateButtonId = createId
    self.theSetterFunction = setterFn
    self.isCreate = creationFlag

  def id(self): return self.theWinId
  def label(self): return self.theWinLabel
  def createButtonId(self): return self.theCreateButtonId
  def dclass(self): return self.theDialogClass
  def setter(self): return self.theSetterFunction
  def createFlag(self): return self.isCreate
