#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RequirementManager.py $ $Id: RequirementManager.py 564 2012-03-12 17:53:00Z shaf $
import ARM
import RequirementFactory
from Borg import Borg

class RequirementManager:  

  def __init__(self,modCombo,isAsset=True):
    b = Borg()
    self.dbProxy = b.dbProxy
    self.modCombo = modCombo
    self.isAsset = isAsset
    modName = self.modCombo.GetValue()
    self.reqs = self.dbProxy.getOrderedRequirements(modName,isAsset)
#    if (len(self.reqs) == 0):
#      self.add('1')

  def __getitem__(self,reqId):
    return self.reqs[reqId]

  def objects(self):
    return self.reqs

  def relabel(self):
    label = 1
    for req in self.reqs:
      req.update('label',label)
      label += 1

  def environment(self):
    return self.dbProxy.environmentId

  def size(self):
    return len(self.reqs)

  def update(self,label,attr,value):
    idx,req = self.requirementByLabel(label)
    req.update(attr,value)    

  def commitChanges(self,idx=-1):
    for r in self.reqs:
      if r.dirty():
        r.incrementVersion()
        self.dbProxy.updateRequirement(r)
        r.dirtyAttrs = set([])
        
  def labelIndex(self,label):
    x = 0
    for key, r in enumerate(self.reqs):
      if (r.label() == label):
        return x
      else:
        x += 1
 
  def requirementById(self,id):
    for idx,r in enumerate(self.reqs):
      if (str(r.id()) == str(id)):
        return (idx,r)
    exceptionText = 'Parent requirement ' + str(id) + ' does not exist'
    raise ARM.RequirementDoesNotExist(exceptionText)
 
  def posByRequirement(self,id):
    for idx,r in enumerate(self.reqs):
      if (str(r.id()) == str(id)):
        return idx
    exceptionText = 'Requirement ' + str(id) + ' does not exist'
    raise ARM.RequirementDoesNotExist(exceptionText)

  def requirementByLabel(self,label):
    for idx,r in enumerate(self.reqs):
      if (r.label() == label):
        return (idx,r)

  def add(self,newLabel,idx=-1,newName="",newDescription="", newPriority="1", newRationale="None", newFitCriterion="None", newOriginator="",newType="Functional",newParent=-1):
    reqId = self.dbProxy.newId()
    modName = self.modCombo.GetStringSelection()
    if (modName == ''):
      modName = self.modCombo.GetString(0)
    r = RequirementFactory.build(reqId,newLabel,newName,newDescription,newPriority,newRationale,newFitCriterion,newOriginator,newType,modName)

    self.dbProxy.addRequirement(r,modName,self.isAsset)
    if (idx != -1):
      self.reqs.insert(idx,r)
      self.relabel()
    else:
      self.reqs.append(r)
    self.commitChanges()
    return r

  def delete(self,idx):
    oldNoReqs = len(self.reqs)
    r = self.reqs[idx]
    reqId = r.id()
    self.reqs.remove(r)    
    self.dbProxy.deleteRequirement(reqId)
    self.relabel()
    return 1

  def asString(self):
    for r in self.reqs:
      print r.asString()
