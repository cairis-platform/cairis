#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/MisuseCaseNodeDialog.py $ $Id: MisuseCaseNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
from Borg import Borg
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
