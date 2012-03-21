#$URL: svn://edison.cs.ox.ac.uk/res08/iris/iris/TVTypeContentHandler.py $ $Id: TVTypeContentHandler.py 329 2010-10-31 14:59:16Z shaf $

from xml.sax.handler import ContentHandler
from ValueTypeParameters import ValueTypeParameters

class DomainValueContentHandler(ContentHandler):
  def __init__(self):
    self.theValuesMap = {}
    self.theValuesMap['threat_value'] = []
    self.theValuesMap['risk_class'] = []
    self.theValuesMap['countermeasure_value'] = []
    self.theValuesMap['severity'] = []
    self.theValuesMap['likelihood'] = []
    self.resetAttributes()

  def resolveEntity(self,publicId,systemId):
    return "/home/irisuser/iris/iris/config/domainvalues.dtd"

  def values(self):
    return (self.theValuesMap['threat_value'],self.theValuesMap['risk_class'],self.theValuesMap['countermeasure_value'],self.theValuesMap['severity'],self.theValuesMap['likelihood'])

  def resetAttributes(self):
    self.inDescription = 0
    self.theTypeName = ''
    self.theDescription = ''

  def startElement(self,name,attrs):
    if (name == 'description'):
      self.inDescription = 1
    elif (name == 'threat_value') or (name == 'countermeasure_value'):
      self.theName = attrs['name']
      self.theTypeName = name
    elif name == 'risk_value':
      self.theName = attrs['name']
      self.theTypeName = 'risk_class'
    elif name == 'severity_value':
      self.theName = attrs['name']
      self.theTypeName = 'severity'
    elif name == 'likelihood_value':
      self.theTypeName = 'likelihood'
      self.theName = attrs['name']

  def characters(self,data):
    if self.inDescription:
      self.theDescription = data
      self.inDescription = 0

  def endElement(self,name):
    if (name == 'threat_value') or (name == 'risk_value') or (name == 'countermeasure_value') or (name == 'severity_value') or (name == 'likelihood_value'):
      p = ValueTypeParameters(self.theName,self.theDescription,self.theTypeName)
      self.theValuesMap[self.theTypeName].append(p)
      self.resetAttributes()
