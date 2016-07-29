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

__author__ = 'Shamal Faily'

from Requirement import Requirement

IMPERATIVES = set(['shall','must','is required to','are applicable','are to','responsible for','will','should'])
OPTIONS = ['can','may','optionally']
WEAKPHRASES = ['adequate','as appropriate','be able to','be capable of','capability of','capability to','effective','as required','normal','provide for','timely','easy to']
FUZZY = ['mostly','as needed','might','make sense','appropriate','might make sense','graceful','at minimum','major','slowly','may be of use','including but not limited to','and/or','suitable','various','clean and stable interface','several']
INCOMPLETES = ['TBD','TBS','TBE','TBC','TBR','not defined','not determined','but not limited to','as a minimum','None']

#from http://requirements.seilevel.com/messageboard/showthread.php?t=257
COMPARATIVES = set(['earliest','latest','highest'])
CONTRACT_TROUBLE = set(['fit for purpose','where applicable','shall be considered'])

def ambiguityScore(desc,fc):
  score = 0
  for w in (OPTIONS + WEAKPHRASES + FUZZY):
# Description only for webinos D2.5    if (w in (desc + fc)):
    if (w in desc):
      score += 1
  return score

def imperativeScore(desc):
  score = 0
  for w in IMPERATIVES:
    if (w in desc): score += 1
  return score

def incompleteScore(desc,rationale,fc,originator):
  score = 0
  if (desc == ''): score += 1
  if (rationale == ''): score += 1
  if (fc == ''): score += 1
  if (originator == ''): score += 1
  for w in INCOMPLETES:
    if (w in desc): 
      score += 1
    if (w in rationale): 
      score += 1
    if (w in fc): 
      score += 1
    if (w in originator): 
      score += 1
  return score

def build(r):
  desc = r.description()
  fc = r.fitCriterion()
  rationale = r.rationale()
  originator = r.originator() 
  incScore = incompleteScore(desc,rationale,fc,originator)
  impScore = imperativeScore(desc)
  ambScore = ambiguityScore(desc,fc)
  
  normIncScore = 1
  if (incScore == 1):
    normIncScore = 0.5
  elif (incScore > 1):
    normIncScore = 0

  normImpScore = 0.8
  if (impScore == 0):
    normImpScore = 0.4

  normAmbScore = 1
  if (ambScore == 0):
    normAmbScore = 1
  elif (ambScore <= 2):
    normAmbScore = 0.5
  else:
    normAmbScore = 0

  s = [normIncScore,normImpScore,normAmbScore]
  return s

