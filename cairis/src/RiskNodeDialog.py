#$URL: svn://edison.comlab.ox.ac.uk/res08/iris/iris/RiskNodeDialog.py $ $Id: RiskNodeDialog.py 249 2010-05-30 17:07:31Z shaf $
import sys
import gtk
from NDImplementationDecorator import NDImplementationDecorator
from Borg import Borg

class RiskNodeDialog:
  def __init__(self,objt,rating,environmentName,builder):
    self.builder = builder
    self.window = self.builder.get_object("RiskNodeDialog")
    self.decorator = NDImplementationDecorator(builder)
    self.decorator.updateTextCtrl("riskNameCtrl",objt.name())
    self.decorator.updateTextCtrl("riskThreatCtrl",objt.threat())
    self.detailsDict = {}


    self.decorator.updateTextCtrl("riskVulnerabilityCtrl",objt.vulnerability())
    self.decorator.updateTextCtrl("riskRatingCtrl",rating)
    b = Borg()
    proxy = b.dbProxy
    
    riskDetails = []
    riskScores = proxy.riskScore(objt.threat(),objt.vulnerability(),environmentName,objt.name())
    for idx,riskScore in enumerate(riskScores):
      riskDetails.append([riskScore[0],riskScore[1]])
      self.detailsDict[riskScore[0]] = riskScore[2]
    self.decorator.updateListCtrl("riskScoreCtrl",['Response','Score'],gtk.ListStore(str,str),riskDetails)
    self.defaultSize = self.window.get_size()
    detailsCtrlWindow = self.builder.get_object("riskDetailsCtrl")
    detailsCtrlWindow.hide()


  def on_riskOkButton_clicked(self,callback_data):
    self.window.destroy()

  def on_riskDetailsButton_clicked(self,callback_data):
    detailsButton = self.builder.get_object("riskDetailsButton")
    detailsCtrlWindow = self.builder.get_object("riskDetailsCtrl")
    label = detailsButton.get_label()
    if (label == 'Show Details'):
      detailsButton.set_label('Hide Details')
      detailsCtrlWindow.show()
      self.window.resize(600,525)
    else: 
      detailsButton.set_label('Show Details')
      detailsCtrlWindow.hide()
      self.window.resize(self.defaultSize[0],self.defaultSize[1])

#treeview, iter, path, user_data
  def onResponseSelected(self,widget):
    scoreCtrl = self.builder.get_object("riskScoreCtrl")
    treeselection = scoreCtrl.get_selection()
    (model, iter) = treeselection.get_selected()
    detailsBuf = self.detailsDict[model.get_value(iter, 0)]
    self.decorator.updateMLTextCtrl("riskDetailsCtrl",detailsBuf)

  def show(self):
    self.window.show()
