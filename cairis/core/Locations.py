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

from .Location import Location

__author__ = 'Shamal Faily'

class Locations:
  def __init__(self,locsId,locsName,locsDiagram,locs,links=[]):
    self.theId = locsId
    self.theName = locsName
    self.theDiagram = locsDiagram
    self.theLocations = locs
    self.theLinks = set(links)
    if len(self.theLinks) == 0:
      for loc in self.theLocations:
        for link in loc.links():
          if ((link,loc.name()) not in self.theLinks) and ((loc.name(),link) not in self.theLinks):
            self.theLinks.add((link,loc.name()))


  def id(self): return self.theId
  def name(self): return self.theName
  def diagram(self): return self.theDiagram
  def locations(self): return self.theLocations
  def links(self): return self.theLinks
