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


import sys
import gtk
from cairis.core.Borg import Borg
from NDImplementationDecorator import NDImplementationDecorator


class MisuseCaseNodeDialog:
  def __init__(self,objt,environmentName,dupProperty,overridingEnvironment,builder):
    self.window = builder.get_object("MisuseCaseNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("misuseCaseNameCtrl",objt.name())

    b = Borg()
    proxy = b.dbProxy
    environmentId = proxy.getDimensionId(environmentName,'environment')
    threatName,vulName = proxy.riskComponents(objt.risk())

    threatId = proxy.getDimensionId(threatName,'threat')
    vulId = proxy.getDimensionId(vulName,'vulnerability')
    self.decorator.updateTextCtrl("misuseCaseThreatCtrl",threatName)
    self.decorator.updateTextCtrl("misuseCaseLikelihoodCtrl",proxy.threatLikelihood(threatId,environmentId))
    self.decorator.updateTextCtrl("misuseCaseVulnerabilityCtrl",vulName)
    self.decorator.updateTextCtrl("misuseCaseSeverityCtrl",proxy.vulnerabilitySeverity(vulId,environmentId))
    self.decorator.updateTextCtrl("misuseCaseRiskRatingCtrl",proxy.riskRating(threatName,vulName,environmentName))

    attackers = proxy.threatAttackers(threatId,environmentId)
    attackerSet = set(attackers)
    attackers = []
    for attacker in attackerSet:
      attackers.append([attacker])
    self.decorator.updateListCtrl("misuseCaseAttackersCtrl",['Attacker'],gtk.ListStore(str),attackers)

    threatenedAssets = proxy.threatenedAssets(threatId,environmentId)
    vulnerableAssets = proxy.vulnerableAssets(vulId,environmentId)
    assetSet = set(threatenedAssets + vulnerableAssets)
    assets = []
    for asset in assetSet:
      assets.append([asset])
    self.decorator.updateListCtrl("misuseCaseAssetsCtrl",['Asset'],gtk.ListStore(str),assets)

    self.decorator.updateMLTextCtrl("misuseCaseNarrativeCtrl",objt.narrative(environmentName,dupProperty))

    objectiveText = 'Exploit vulnerabilities in '
    for idx,vulAsset in enumerate(vulnerableAssets):
      objectiveText += vulAsset
      if (idx != (len(vulnerableAssets) -1)):
        objectiveText += ','
    objectiveText += ' to threaten '
    for idx,thrAsset in enumerate(threatenedAssets):
      objectiveText += thrAsset
      if (idx != (len(threatenedAssets) -1)):
        objectiveText += ','
    objectiveText += '.'
    self.decorator.updateTextCtrl("misuseCaseObjectiveCtrl",objectiveText)


    self.window.resize(350,100)

  def on_misuseCaseOkButton_clicked(self,callback_data):
    self.window.destroy()

  def show(self):
    self.window.show()
