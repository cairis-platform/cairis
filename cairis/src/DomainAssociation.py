#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DomainAssociation.py $ $Id: DomainAssociation.py 249 2010-05-30 17:07:31Z shaf $
class DomainAssociation:
  def __init__(self,headType,headName,tailType,tailName,desc='',connectionDomain = ''):
    self.theHeadType = headType
    self.theHeadDomain = headName
    self.theTailType = tailType
    self.theTailDomain = tailName
    self.thePhenomena = desc
    self.theConnectionDomain = connectionDomain

  def headType(self): return self.theHeadType
  def headDomain(self): return self.theHeadDomain
  def tailType(self): return self.theTailType
  def tailDomain(self): return self.theTailDomain
  def phenomena(self): return self.thePhenomena
  def connectionDomain(self): return self.theConnectionDomain
