#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DomainAssociationParameters.py $ $Id: DomainAssociationParameters.py 249 2010-05-30 17:07:31Z shaf $
import ObjectCreationParameters

class DomainAssociationParameters(ObjectCreationParameters.ObjectCreationParameters):
  def __init__(self,headName,tailName,desc='',cDom=''):
    ObjectCreationParameters.ObjectCreationParameters.__init__(self)
    self.theHeadDomain = headName
    self.theTailDomain = tailName
    self.thePhenomena = desc
    self.theConnectionDomain = cDom

  def headDomain(self): return self.theHeadDomain
  def tailDomain(self): return self.theTailDomain
  def phenomena(self): return self.thePhenomena
  def connectionDomain(self): return self.theConnectionDomain
