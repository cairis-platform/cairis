#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/EnvironmentProperties.py $ $Id: EnvironmentProperties.py 249 2010-05-30 17:07:31Z shaf $
class EnvironmentProperties:
  def __init__(self,name):
    self.theEnvironmentName = name

  def name(self): return self.theEnvironmentName
