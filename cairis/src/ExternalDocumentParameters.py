#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ExternalDocumentParameters.py $ $Id: ExternalDocumentParameters.py 419 2011-01-25 21:34:13Z shaf $
from ObjectCreationParameters import ObjectCreationParameters

class ExternalDocumentParameters(ObjectCreationParameters):
  def __init__(self,edName,edVersion,edDate,edAuths,edDesc):
    ObjectCreationParameters.__init__(self)
    self.theName = edName
    self.theVersion = edVersion
    self.thePublicationDate = edDate
    self.theAuthors = edAuths
    self.theDescription = edDesc

  def name(self): return self.theName
  def version(self): return self.theVersion
  def date(self): return self.thePublicationDate
  def authors(self): return self.theAuthors
  def description(self): return self.theDescription
