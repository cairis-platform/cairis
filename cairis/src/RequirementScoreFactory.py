#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RequirementScoreFactory.py $ $Id: RequirementScoreFactory.py 579 2012-03-19 16:20:12Z shaf $
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

