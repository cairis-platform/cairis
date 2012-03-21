#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ARM.py $ $Id: ARM.py 330 2010-10-31 15:01:28Z shaf $
class ARMException(Exception):
  def __init__(self,value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class EnvironmentValidationError(ARMException):
  def __init__(self,value):
    ARMException.__init__(self,value)

class DatabaseProxyException(ARMException):
  def __init__(self,value):
    ARMException.__init__(self,value)

class IntegrityException(DatabaseProxyException):
  def __init__(self,value):
    DatabaseProxyException.__init__(self,value)

class RequirementDoesNotExist(ARMException):
  def __init__(self,value):
    ARMException.__init__(self,value)

class UnknownParameterClass(ARMException):
  def __init__(self,value):
    ARMException.__init__(self,value)

class UnknownPanelClass(ARMException):
  def __init__(self,value):
    ARMException.__init__(self,value)

class UnknownNodeType(ARMException):
  def __init__(self,value):
    ARMException.__init__(self,value)

class UnknownDialogClass(ARMException):
  def __init__(self,value):
    ARMException.__init__(self,value)

class UnknownOperatingSystem(ARMException):
  def __init__(self,value):
    ARMException.__init__(self,value)

class ConflictingType(ARMException):
  def __init__(self,value):
    ARMException.__init__(self,value)
