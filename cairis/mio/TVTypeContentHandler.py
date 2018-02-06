#  Licensed to the Apache Software Foundation (ASF) under one
#  or more contributor license agreements.  See the NOTICE file
#  distributed with this work for additional information
#  regarding copyright ownership.  The ASF licenses this file
#  to you under the Apache License, Version 2.0 (the
#  "License"); you may not use this file except in compliance
#  with the License.  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#  KIND, either express or implied.  See the License for the
#  specific language governing permissions and limitations
#  under the License.


from xml.sax.handler import ContentHandler,EntityResolver
from cairis.core.ValueTypeParameters import ValueTypeParameters
from cairis.core.Borg import Borg
from xml.sax.saxutils import unescape

__author__ = 'Shamal Faily'

class TVTypeContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theVulnerabilityTypes = []
    self.theThreatTypes = []
    self.resetAttributes()
    b = Borg()
    self.configDir = b.configDir

  def resolveEntity(self,publicId,systemId):
    return systemId

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
      p = ValueTypeParameters(unescape(self.theName),unescape(self.theDescription),'vulnerability_type')
      self.theVulnerabilityTypes.append(p)
      self.resetAttributes() 
    if name == 'threat_type':
      p = ValueTypeParameters(unescape(self.theName),unescape(self.theDescription),'threat_type')
      self.theThreatTypes.append(p)
      self.resetAttributes() 
