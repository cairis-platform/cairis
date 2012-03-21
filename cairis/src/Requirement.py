#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Requirement.py $ $Id: Requirement.py 564 2012-03-12 17:53:00Z shaf $
class Requirement:
  def __init__(self,id,label,name='',description='',priority='1',rationale='',fitCriterion='',originator='',type='Functional',asset='',version=-1):
    self.theId = id
    if (version == -1):
      self.theVersion = 1
    else:
      self.theVersion = version
    self.attrs = {}
    self.theLabel = label
    self.theName = name
    self.theDescription = description
    self.thePriority = priority
    self.attrs['rationale'] = rationale
    self.attrs['originator'] = originator
    self.attrs['fitCriterion'] = fitCriterion
    self.attrs['supportingMaterial'] = ''
    self.attrs['type'] = type
    self.attrs['asset'] = asset
    self.dirtyAttrs = set([])

  def label(self):
    return self.theLabel

  def name(self):
    return self.theName

  def description(self):
    return self.theDescription

  def priority(self):
    return self.thePriority

  def rationale(self):
    return self.attrs['rationale']

  def fitCriterion(self):
    return self.attrs['fitCriterion']

  def version(self):
    return self.theVersion

  def originator(self):
    return self.attrs['originator']

  def type(self):
    return self.attrs['type']

  def asset(self):
    return self.attrs['asset']

  def dirty(self):
    return len(self.dirtyAttrs)

  def update(self,attr,val):
    if (attr == 'label'):
      self.theLabel = val
    elif (attr == 'name'):
      self.theName = val
    elif (attr == 'description'):
      self.theDescription = val
    elif (attr == 'priority'):
      self.thePriority = val
    else:
      self.attrs[attr] = str(val)
    self.dirtyAttrs.add(attr)

  def incrementVersion(self):
    self.theVersion += 1

  def id(self):
    return self.theId

  def asString(self):
    return 'id:' + str(self.theId) + ', label:' + str(self.theLabel) + ', name: ' + self.theName + ', description:' + self.theDescription + ', priority:' + str(self.thePriority) + ', rationale:' + self.attrs['rationale'] + ', fit criterion:' + self.attrs['fitCriterion'] + ', originator:' + self.attrs['originator'] + ',type:' + self.attrs['type'] + ',domain:' + self.attrs['domain'] + ',version:' + str(self.theVersion)
