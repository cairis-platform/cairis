#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/Environment.py $ $Id: Environment.py 439 2011-03-19 22:01:02Z shaf $
class Environment:
  def __init__(self,id,name,sc,description,environments,duplProperty,overridingEnvironment,envTensions):
    self.theId = id
    self.theName = name
    self.theShortCode = sc
    self.theDescription = description
    self.theEnvironments = environments
    self.theDuplicateProperty = duplProperty
    self.theOverridingEnvironment = overridingEnvironment
    self.theTensions = envTensions

  def id(self): return self.theId
  def name(self): return self.theName
  def shortCode(self): return self.theShortCode
  def description(self): return self.theDescription
  def environments(self): return self.theEnvironments
  def duplicateProperty(self): return self.theDuplicateProperty
  def overridingEnvironment(self): return self.theOverridingEnvironment
  def tensions(self): return self.theTensions

  def __str__(self): return 'id: ' + str(self.theId) + ', name: ' + self.theName + ', short code:' + self.theShortCode + ', description: ' + self.theDescription + ', environments: ' + str(self.theEnvironments) + ', dupProperty: ' + self.theDuplicateProperty + ', overridingEnv: ' + self.theOverridingEnvironment
