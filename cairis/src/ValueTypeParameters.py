#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ValueTypeParameters.py $ $Id: ValueTypeParameters.py 427 2011-02-27 12:29:59Z shaf $
import ObjectCreationParameters

class ValueTypeParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,vtName,vtDesc,vType,envName = ''):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theName = vtName
    self.theDescription = vtDesc
    self.theType = vType
    self.theEnvironmentName = envName

  def name(self): return self.theName
  def description(self): return self.theDescription
  def type(self): return self.theType
  def environment(self): return self.theEnvironmentName
