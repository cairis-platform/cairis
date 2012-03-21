#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ObjectCreationParameters.py $ $Id: ObjectCreationParameters.py 249 2010-05-30 17:07:31Z shaf $

class ObjectCreationParameters:
  def __init__(self):
    self.theId = -1
    pass

  def setId(self,anId):
    self.theId = anId

  def id(self):
    return self.theId
