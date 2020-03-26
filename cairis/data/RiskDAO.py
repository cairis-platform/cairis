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

from cairis.core.ARM import *
from cairis.daemon.CairisHTTPError import ARMHTTPError, ObjectNotFoundHTTPError, MalformedJSONHTTPError, MissingParameterHTTPError, \
    OverwriteNotAllowedHTTPError, SilentHTTPError
import cairis.core.MisuseCaseFactory
from cairis.core.MisuseCaseParameters import MisuseCaseParameters
from cairis.core.MisuseCase import MisuseCase
from cairis.core.MisuseCaseEnvironmentProperties import MisuseCaseEnvironmentProperties
from cairis.core.RiskParameters import RiskParameters
from cairis.data.AssetDAO import AssetDAO
from cairis.data.CairisDAO import CairisDAO
from cairis.core.Risk import Risk
from cairis.misc.EnvironmentModel import EnvironmentModel
from cairis.tools.JsonConverter import json_deserialize
from cairis.tools.ModelDefinitions import RiskModel, MisuseCaseModel, MisuseCaseEnvironmentPropertiesModel
from cairis.tools.PseudoClasses import RiskScore, RiskRating
from cairis.tools.SessionValidator import check_required_keys, get_fonts

__author__ = 'Robin Quetin, Shamal Faily'


class RiskDAO(CairisDAO):
  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id, 'risk')

  def get_objects(self, constraint_id=-1, simplify=True, skip_misuse=False):
    try:
      risks = self.db_proxy.getRisks(constraintId=constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    riskKeys = sorted(risks.keys())
    riskList = []
    for key in riskKeys:
      value = risks[key]
      if value.theMisuseCase:
        value.theMisuseCase = self.get_misuse_case_by_risk_name(value.theName, simplify=False)
        riskList.append(self.simplify(value))
    return riskList


  def get_objects_summary(self):
    try:
      risks = self.db_proxy.getRisksSummary()
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    return risks

  def get_risk_names(self):
    risks = self.get_objects(skip_misuse=True)
    risk_names = list(risks.keys())
    return risk_names

  def risk_model_elements(self,envName, pathValues = []):
    try:
      return self.db_proxy.riskModelElements(envName)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)



  def get_object_by_name(self, name, simplify=True, skip_misuse=False):
    try:
      riskId = self.db_proxy.getDimensionId(name,'risk')
      risks = self.db_proxy.getRisks(riskId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if risks is not None:
      found_risk = risks.get(name)

    if found_risk is None:
      self.close()
      raise ObjectNotFoundHTTPError(obj='The provided risk name')
  
    if found_risk.theMisuseCase and not skip_misuse:
      found_risk.theMisuseCase = self.get_misuse_case_by_risk_name(found_risk.theName, simplify=False)
    if simplify:
      found_risk = self.simplify(found_risk)
    return found_risk

  def get_risk_analysis_model(self, environment_name, pathValues = []):
    fontName, fontSize, apFontName = get_fonts(session_id=self.session_id)
    dim_name = pathValues[0]
    obj_name = pathValues[1]
    isTagged = pathValues[2]
    rankDir = pathValues[3]
    model_layout = pathValues[4]

    if (isTagged == '1'):
      isTagged = True
    else:
      isTagged = False

    if dim_name == 'all':
      dim_name = ''
    if obj_name == 'all':
      obj_name = ''

    if model_layout == 'Hierarchical':
      model_layout = 'dot'
    elif model_layout == 'Spring':
      model_layout = 'fdp'
    elif model_layout == 'Radial':
      model_layout = 'twopi'
    else:
      model_layout = 'circo'

    if rankDir == 'Horizontal':
      rankDir = 'LR'
    else:
      rankDir = 'TB'
   
    try:
      riskAnalysisModel = self.db_proxy.riskAnalysisModel(environment_name, dim_name, obj_name)
      tLinks = EnvironmentModel(riskAnalysisModel, environment_name, self.db_proxy, model_layout, fontName=fontName, fontSize=fontSize, isTagged=isTagged, rankDir=rankDir)
      dot_code = tLinks.graph()
      if not dot_code:
        raise ObjectNotFoundHTTPError('The risk analysis model')
      return dot_code
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except Exception as ex:
      self.close()
      print(ex)

  def delete_object(self, name):
    found_risk = self.get_object_by_name(name)

    try:
      riskId = self.db_proxy.getDimensionId(name,'risk')
      self.db_proxy.deleteRisk(riskId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def add_object(self, risk):
    try:
      self.db_proxy.nameCheck(risk.name(), 'risk')
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    params = RiskParameters(riskName=risk.name(),threatName=risk.threat(),vulName=risk.vulnerability(),mc=risk.misuseCase(),rTags=risk.tags())

    try:
      self.db_proxy.addRisk(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def update_object(self, risk, risk_name):
    params = RiskParameters(riskName=risk.theName,threatName=risk.theThreatName,vulName=risk.theVulnerabilityName,mc=risk.theMisuseCase,rTags=risk.theTags)
    try:
      riskId = self.db_proxy.getDimensionId(risk_name,'risk')
      params.setId(riskId)
      self.db_proxy.updateRisk(params)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def check_existing_risk(self, risk_name):
    try:
      self.get_risk_by_name(risk_name)
      return True
    except ObjectNotFoundHTTPError:
      self.db_proxy.reconnect(session_id=self.session_id)
      return False

  def get_misuse_cases(self, pathValues = []):
    constraint_id = pathValues[0]
    try:
      misuse_cases = self.db_proxy.getMisuseCases(constraintId=constraint_id)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    mcKeys = sorted(misuse_cases.keys())
    mcList = []
    for key in mcKeys:
      threat_name, vuln_name = self.db_proxy.misuseCaseRiskComponents(key)
      misuse_cases[key].theThreatName = threat_name
      misuse_cases[key].theVulnerabilityName = vuln_name
      for mcep in misuse_cases[key].environmentProperties():
        envName = mcep.name()
        misuse_cases[key].theObjective = self.get_misuse_case_obj_and_assets(threat_name,vuln_name,envName)
        mcList.append(self.simplify(misuse_cases[key]))
    return mcList

  def get_misuse_case_by_name(self, misuse_case_name, pathValues = []):
    try:
      misuse_cases = self.db_proxy.getMisuseCases()
      for key in misuse_cases:
        if key == misuse_case_name:
          return misuse_cases[key]
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    

  def get_misuse_case_by_risk_name(self, risk_name, simplify=True, pathValues = []):
    try:
      riskId = self.db_proxy.getDimensionId(risk_name,'risk')
      misuse_case = self.db_proxy.riskMisuseCase(riskId)
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

    if not misuse_case:
      self.close()
      raise ObjectNotFoundHTTPError('The misuse case associated with the risk')
    assert isinstance(misuse_case, MisuseCase)

    misuse_case = self.expand_mc_props(misuse_case)

    if simplify:
      misuse_case = self.simplify(misuse_case)
    if hasattr(misuse_case,'theId'):
      del misuse_case.theId
      del misuse_case.theEnvironmentDictionary

    return misuse_case

  def get_misuse_case_by_threat_vulnerability(self, threat_name,vulnerability_name, pathValues = []):
    try:
      misuse_case = self.db_proxy.riskMisuseCase(-1,threat_name,vulnerability_name)
      if misuse_case != None:
        return self.simplify(misuse_case)
      else:
        return self.simplify(cairis.core.MisuseCaseFactory.build(threat_name,vulnerability_name,self.db_proxy))
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def get_misuse_case_assets(self, threat_name, environment_name):
    """
    :rtype : list[str]
    """
    attackers = []
    try:
      threat_id = self.db_proxy.getDimensionId(threat_name, 'threat')
      environment_id = self.db_proxy.getDimensionId(environment_name, 'environment')
      attackers = self.db_proxy.threatAttackers(threat_id, environment_id)
    except DatabaseProxyException as ex:
      SilentHTTPError(ex.value)
    except ARMException as ex:
      SilentHTTPError(str(ex.value))

    return attackers

  def get_misuse_case_attackers(self, threat_name, environment_name):
    """
    :rtype : list[str]
    """
    attackers = []
    try:
      threat_id = self.db_proxy.getDimensionId(threat_name, 'threat')
      environment_id = self.db_proxy.getDimensionId(environment_name, 'environment')
      attackers = self.db_proxy.threatAttackers(threat_id, environment_id)
    except DatabaseProxyException as ex:
      SilentHTTPError(ex.value)
    except ARMException as ex:
      SilentHTTPError(str(ex.value))

    return attackers

  def get_misuse_case_obj_and_assets(self, threat_name, vulnerability_name, environment_name):
    """
    :rtype : str, list[Asset]
    """
    dao = AssetDAO(self.session_id)
    threatened_assets = []
    vulnerable_assets = []
    try:
      threatened_assets = dao.get_threatened_assets(threat_name, environment_name)
      vulnerable_assets = dao.get_vulnerable_assets(vulnerability_name, environment_name)
    except ObjectNotFoundHTTPError as ex:
      SilentHTTPError(ex.message)

    objectiveText = 'Exploit vulnerabilities in '
    for idx,vulAsset in enumerate(vulnerable_assets):
      objectiveText += vulAsset
      if (idx != (len(vulnerable_assets) -1)):
        objectiveText += ','
    objectiveText += ' to threaten '
    for idx,thrAsset in enumerate(threatened_assets):
      objectiveText += thrAsset
      if (idx != (len(threatened_assets) -1)):
        objectiveText += ','
    objectiveText += '.'
    assets = set(threatened_assets + vulnerable_assets)

    return objectiveText, list(assets)

  def get_misuse_case_likelihood(self, threat_name, environment_name):
    likelihood_name = 'N/A'
    try:
      threat_id = self.db_proxy.getDimensionId(threat_name, 'threat')
      environment_id = self.db_proxy.getDimensionId(environment_name, 'environment')
      likelihood_name = self.db_proxy.threatLikelihood(threat_id, environment_id)
    except DatabaseProxyException as ex:
      SilentHTTPError(ex.value)
    except ARMException as ex:
      SilentHTTPError(str(ex.value))

    return likelihood_name

  def get_misuse_case_severity(self, vulnerability_name, environment_name):
    severity_name = 'N/A'
    try:
      vulnerability_id = self.db_proxy.getDimensionId(vulnerability_name, 'vulnerability')
      environment_id = self.db_proxy.getDimensionId(environment_name, 'environment')
      severity_name = self.db_proxy.vulnerabilitySeverity(vulnerability_id, environment_id)
    except DatabaseProxyException as ex:
      SilentHTTPError(ex.value)
    except ARMException as ex:
      SilentHTTPError(str(ex.value))

    return severity_name

  def expand_mc_props(self, misuse_case):
    try:
      threat_name, vuln_name = self.db_proxy.misuseCaseRiskComponents(misuse_case.theName)
      misuse_case.theThreatName = threat_name
      misuse_case.theVulnerabilityName = vuln_name
    except DatabaseProxyException as ex:
      self.close()
      if ex.value.find('Error obtaining risk components associated with Misuse Case'):
        raise ObjectNotFoundHTTPError('The associated threat and vulnerability name')
      else:
        raise ARMHTTPError(ex)
    except ARMException as ex:
        self.close()
        raise ARMHTTPError(ex)

    for idx in range(0, len(misuse_case.theEnvironmentProperties)):
      env_prop = misuse_case.theEnvironmentProperties[idx]
      assert isinstance(env_prop, MisuseCaseEnvironmentProperties)
      env_prop.theObjective, env_prop.theAssets = self.get_misuse_case_obj_and_assets(
        misuse_case.theThreatName,
        misuse_case.theVulnerabilityName,
        env_prop.theEnvironmentName
      )
      env_prop.theLikelihood = self.get_misuse_case_likelihood(threat_name, env_prop.theEnvironmentName)
      env_prop.theSeverity = self.get_misuse_case_severity(vuln_name, env_prop.theEnvironmentName)
      env_prop.theRiskRating = self.get_risk_rating_by_tve(threat_name, vuln_name, env_prop.theEnvironmentName)
      env_prop.theAttackers = self.get_misuse_case_attackers(threat_name, env_prop.theEnvironmentName)
      misuse_case.theEnvironmentProperties[idx] = env_prop

    return misuse_case

  def get_scores_by_rvte(self, risk_name, vulnerability_name, threat_name, environment_name, pathValues = []):
    return self.get_scores_by_rtve(risk_name, vulnerability_name, threat_name, environment_name, pathValues)

  def get_scores_by_rtve(self, risk_name, threat_name, vulnerability_name, environment_name, pathValues = []):
    try:
      scores = self.db_proxy.riskScore(threat_name, vulnerability_name, environment_name, risk_name)
      if len(scores) > 0:
        scores = self.convert_scores(real_scores=scores)
      return scores
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)

  def convert_scores(self, real_scores=None, fake_scores=None):
    new_scores = []
    if real_scores:
      if len(real_scores) > 0:
        for idx in range(0, len(real_scores)):
          real_score = real_scores[idx]
          if len(real_score) == 4:
            new_score = RiskScore(response_name=real_score[0],unmit_score=real_score[1],mit_score=real_score[2],details=real_score[3])
            new_scores.append(new_score)
    elif fake_scores:
      if len(fake_scores) > 0:
        for idx in range(0, len(fake_scores)):
          fake_score = fake_scores[idx]
          assert isinstance(fake_score, RiskScore)
          check_required_keys(fake_score, RiskScore.required)
          if fake_score['unmitScore'] == -1:
            fake_score['unmitScore'] = None
          if fake_score['mitScore'] == -1:
            fake_score['mitScore'] = None
          new_score = (fake_score['responseName'], fake_score['unmitScore'], fake_score['mitScore'], fake_score['details'])
          new_scores.append(new_score)
    else:
      self.close()
      raise MissingParameterHTTPError(param_names=['scores'])

    return new_scores

  def get_risk_rating_by_vte(self, vulnerability_name, threat_name, environment_name, pathValues = []):
    return self.get_risk_rating_by_tve(threat_name, vulnerability_name, environment_name, pathValues)

  def get_risk_rating_by_tve(self, threat_name, vulnerability_name, environment_name, pathValues = []):
    try:
      rating = self.db_proxy.riskRating(-1,threat_name, vulnerability_name, environment_name)
      risk_rating = RiskRating(threat_name, vulnerability_name, environment_name, rating)
      return risk_rating
    except DatabaseProxyException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
    except TypeError:
      self.close()
      raise ObjectNotFoundHTTPError(obj='A rating for the risk')
  # endregion

  def from_json(self, request):
    json = request.get_json(silent=True)
    if json is False or json is None:
      self.close()
      raise MalformedJSONHTTPError(data=request.get_data())

    json_dict = json['object']
    check_required_keys(json_dict, RiskModel.required)
    json_dict['__python_obj__'] = RiskParameters.__module__+'.'+RiskParameters.__name__
       
    if json_dict['theMisuseCase']:
      mc_dict = json_dict['theMisuseCase']
      check_required_keys(mc_dict, MisuseCaseModel.required)
      mc_dict['__python_obj__'] = MisuseCaseParameters.__module__+'.'+MisuseCaseParameters.__name__
      for idx in range(0, len(mc_dict['theEnvironmentProperties'])):
        mcep_dict = mc_dict['theEnvironmentProperties'][idx]
        check_required_keys(mcep_dict, MisuseCaseEnvironmentPropertiesModel.required)
        mcep_dict['__python_obj__'] = MisuseCaseEnvironmentProperties.__module__+'.'+MisuseCaseEnvironmentProperties.__name__
        mc_dict['theEnvironmentProperties'][idx] = mcep_dict
      json_dict['theMisuseCase'] = mc_dict

    risk = json_deserialize(json_dict)

    if isinstance(risk, RiskParameters):
      return risk
    else:
      raise MalformedJSONHTTPError()

  def simplify(self, obj):
    misuse_case = None
    if isinstance(obj, Risk):
      misuse_case = obj.theMisuseCase
    elif isinstance(obj, MisuseCase):
      if hasattr(obj,'theId'):
        del obj.theId
        del obj.theEnvironmentDictionary
      misuse_case = obj

    if isinstance(obj, Risk):
      obj.theMisuseCase = misuse_case
      del obj.theId
    elif isinstance(obj, MisuseCase):
      obj = misuse_case
    return obj
