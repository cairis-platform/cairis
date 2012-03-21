#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ExternalDocument.py $ $Id: ExternalDocument.py 419 2011-01-25 21:34:13Z shaf $

class ExternalDocument:
  def __init__(self,edId,edName,edVersion,edDate,edAuths,edDesc):
    self.theId = edId
    self.theName = edName
    self.theVersion = edVersion
    self.thePublicationDate = edDate
    self.theAuthors = edAuths
    self.theDescription = edDesc

  def id(self): return self.theId
  def name(self): return self.theName
  def version(self): return self.theVersion
  def date(self): return self.thePublicationDate
  def authors(self): return self.theAuthors
  def description(self): return self.theDescription
