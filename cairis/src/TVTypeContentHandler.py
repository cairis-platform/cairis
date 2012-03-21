#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/TVTypeContentHandler.py $ $Id: TVTypeContentHandler.py 567 2012-03-13 22:31:40Z shaf $

from xml.sax.handler import ContentHandler
from ValueTypeParameters import ValueTypeParameters

class TVTypeContentHandler(ContentHandler):
  def __init__(self):
    self.theVulnerabilityTypes = []
    self.theThreatTypes = []
    self.resetAttributes()

  def resolveEntity(self,publicId,systemId):
    return "/home/irisuser/iris/iris/config/tvtypes.dtd"

  def types(self):
    return (self.theVulnerabilityTypes,self.theThreatTypes)

  def resetAttributes(self):
    self.inDescription = 0
    self.theTypeName = ''
    self.theDescription = ''


  def startElement(self,name,attrs):
    if (name == 'vulnerability_type' or name == 'threat_type'):
      self.theName = attrs['name']
    elif (name == 'description'):
      self.inDescription = 1

  def characters(self,data):
    if self.inDescription:
      self.theDescription = data
      self.inDescription = 0

  def endElement(self,name):
    if (name == 'vulnerability_type'):
      p = ValueTypeParameters(self.theName,self.theDescription,'vulnerability_type')
      self.theVulnerabilityTypes.append(p)
      self.resetAttributes() 
    if name == 'threat_type':
      p = ValueTypeParameters(self.theName,self.theDescription,'threat_type')
      self.theThreatTypes.append(p)
      self.resetAttributes() 
