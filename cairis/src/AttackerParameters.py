#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/AttackerParameters.py $ $Id: AttackerParameters.py 330 2010-10-31 15:01:28Z shaf $
from ObjectCreationParameters import ObjectCreationParameters

class AttackerParameters(ObjectCreationParameters):
  def __init__(self,name,desc,image,properties):
    ObjectCreationParameters.__init__(self)
    self.theName = name
    self.theDescription = desc
    self.theImage = image
    self.theEnvironmentProperties = properties


  def name(self): return self.theName
  def description(self): return self.theDescription
  def image(self): return self.theImage
  def environmentProperties(self): return self.theEnvironmentProperties
