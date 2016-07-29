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

__author__ = 'Shamal Faily'

class DirectoryContentHandler(ContentHandler,EntityResolver):
  def __init__(self):
    self.theVulnerabilityDirectory = []
    self.theThreatDirectory = []
    b = Borg()
    self.configDir = b.configDir
    self.resetAttributes()

  def resolveEntity(self,publicId,systemId):
    return systemId

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
      self.theVulnerabilityDirectory.append((self.theLabel,self.theName,self.theDescription,self.theType,self.theReference))
      self.resetAttributes() 
    if name == 'threat':
      self.theThreatDirectory.append((self.theLabel,self.theName,self.theDescription,self.theType,self.theReference))
      self.resetAttributes() 
