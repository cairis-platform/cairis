#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/ThreatDialogParameters.py $ $Id: ThreatDialogParameters.py 249 2010-05-30 17:07:31Z shaf $
import DialogClassParameters

class ThreatDialogParameters(DialogClassParameters.DialogClassParameters):
  def __init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag,likelihoodList):
    DialogClassParameters.DialogClassParameters.__init__(self,winId,winLabel,dClass,createId,setterFn,creationFlag)
    self.theLikelihoods = likelihoodList

  def assets(self): return self.theAssets
  def likelihoods(self): return self.theLikelihoods
