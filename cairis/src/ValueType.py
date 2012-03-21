#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ValueType.py $ $Id: ValueType.py 249 2010-05-30 17:07:31Z shaf $

class ValueType:
  def __init__(self,valueTypeId,valueTypeName,valueTypeDescription,vType):
    self.theId = valueTypeId
    self.theName = valueTypeName
    self.theDescription = valueTypeDescription
    self.theType = vType

  def id(self): return self.theId
  def name(self): return self.theName
  def description(self): return self.theDescription
  def type(self): return self.theType
