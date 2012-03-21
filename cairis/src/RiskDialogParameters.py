#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RiskDialogParameters.py $ $Id: RiskDialogParameters.py 249 2010-05-30 17:07:31Z shaf $

import DialogClassParameters

class RiskDialogParameters(DialogClassParameters.DialogClassParameters):
  def __init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag,threatList,vulList,levelList):
    DialogClassParameters.DialogClassParameters.__init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag)
    self.theThreats = threatList
    self.theVulnerabilities = vulList
    self.theLevels = levelList

  def threats(self): return self.theThreats
  def vulnerabilities(self): return self.theVulnerabilities
  def levels(self): return self.theLevels
