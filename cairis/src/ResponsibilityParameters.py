#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ResponsibilityParameters.py $ $Id: ResponsibilityParameters.py 249 2010-05-30 17:07:31Z shaf $
from ObjectCreationParameters import ObjectCreationParameters

class ResponsibilityParameters(ObjectCreationParameters):
  def __init__(self,name):
    ObjectCreationParameters.__init__(self)
    self.theName = name

  def name(self): return self.theName
