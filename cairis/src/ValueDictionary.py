#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ValueDictionary.py $ $Id: ValueDictionary.py 249 2010-05-30 17:07:31Z shaf $ 

class ValueDictionary:
  def __init__(self,values):
    self.theValueLookup = {}
    self.theIdLookup = {}
    for idx,value in enumerate(values):
      self.theValueLookup[idx] = value
      self.theIdLookup[value] = idx

  def id(self,valueName):
    return self.theIdLookup[valueName]

  def name(self,valueId):
    return self.theValueLookup[valueId]

  def values(self):
    return self.theValueLookup.values()
