#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/EnvironmentSingleton.py $ $Id: EnvironmentSingleton.py 249 2010-05-30 17:07:31Z shaf $
from Borg import Borg

class EnvironmentSingleton(Borg):
  environmentId = None
  def __init__(self,cId = None):
    if cId is not None: self.environmentId = cId
  def __str__(self): return str(self.environmentId)
  def __int__(self): return self.environmentId
