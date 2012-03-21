#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/DirectoryContentHandler.py $ $Id: DirectoryContentHandler.py 567 2012-03-13 22:31:40Z shaf $

from xml.sax.handler import ContentHandler
from ValueTypeParameters import ValueTypeParameters

class DirectoryContentHandler(ContentHandler):
  def __init__(self):
    self.theVulnerabilityDirectory = []
    self.theThreatDirectory = []
    self.vdId = 0
    self.tdId = 0
    self.resetAttributes()

  def resolveEntity(self,publicId,systemId):
    return "/home/irisuser/iris/iris/config/directory.dtd"

  def directories(self):
    return (self.theVulnerabilityDirectory,self.theThreatDirectory)

  def resetAttributes(self):
    self.inDescription = 0
    self.theLabel = ''
    self.theName = ''
    self.theType = ''
    self.theReference = ''
    self.theDescription = ''


  def startElement(self,name,attrs):
    if (name == 'vulnerability' or name == 'threat'):
      self.theLabel = attrs['label']
      self.theName = attrs['name']
      self.theType = attrs['type']
      self.theReference = attrs['reference']
    elif (name == 'description'):
      self.inDescription = 1

  def characters(self,data):
    if self.inDescription:
      self.theDescription = data
      self.inDescription = 0

  def endElement(self,name):
    if (name == 'vulnerability'):
      self.theVulnerabilityDirectory.append((self.vdId,self.theLabel,self.theName,self.theDescription,self.theType,self.theReference))
      self.vdId += 1 
      self.resetAttributes() 
    if name == 'threat':
      self.theThreatDirectory.append((self.tdId,self.theLabel,self.theName,self.theDescription,self.theType,self.theReference))
      self.tdId += 1 
      self.resetAttributes() 
