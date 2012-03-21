#$URL$ $Id$
from Borg import Borg
import DotTrace
import pydot
import wx
import os
import ARM
import gtk

class ConceptMapModel:
  def __init__(self,associations,envName,conceptName = '',cfSet = False):
    self.theAssociations = associations
    self.theEnvironmentName = envName
    self.theConceptName = conceptName
    b = Borg()
    self.dbProxy = b.dbProxy
    self.fontName = b.fontName
    self.fontSize = b.fontSize
    self.theGraph = pydot.Dot()
    if (cfSet == True):
      self.theGraph.set_node_defaults(shape='ellipse',colorscheme='set14',color='1',fontname=self.fontName,fontsize=self.fontSize,style='filled')
    else:
      self.theGraph.set_node_defaults(shape='rectangle',colorscheme='spectral3',color='1',fontname=self.fontName,fontsize=self.fontSize)
    self.theGraph.set_edge_defaults(arrowhead='vee')
    self.cfSet = cfSet
    self.theClusters = {}
    self.theEdges = []
    if (os.name == 'nt'):
      self.theGraphName = 'C:\\arm\\concept.dot'
    elif (os.uname()[0] == 'Linux'):
      self.theGraphName = os.environ['IRIS_SCRATCH'] + '/concept.dot'
    elif (os.uname()[0] == 'Darwin'):
      self.theGraphName = os.environ['IRIS_SCRATCH'] + '/concept.dot'
    else :
      raise ARM.UnsupportedOperatingSystem(os.name)

  def size(self):
    return len(self.theAssociations)

  def buildNode(self,objtName,envName):
    objtUrl = 'requirement#' + objtName
    envLabel = envName.replace(' ','_')
    if envName not in self.theClusters:
      self.theClusters[envName] = pydot.Cluster(envLabel,label=str(envName))
    reqObjt = self.dbProxy.dimensionObject(objtName,'requirement')
    tScore = self.dbProxy.traceabilityScore(objtName)
    fontColour = 'black'
    if (reqObjt.priority() == 1):
      if tScore != 3: fontColour = 1

    n = pydot.Node(objtName,color=str(tScore),fontcolor=str(fontColour),URL=objtUrl)
    if (self.cfSet == False):
      n.obj_dict['attributes']['style'] = '"rounded,filled"'
    self.theClusters[envName].add_node(n)

  def layout(self,renderer = 'dot'):
    self.theGraph.write_xdot(self.theGraphName,prog=renderer)
    return open(self.theGraphName).read()

  def graph(self):
    self.conceptNameSet = set([])
    self.assocSet = set([])

    for association in self.theAssociations:
      fromName = association.fromName()
      toName = association.toName()
      lbl = association.label()
      fromEnv = association.fromEnvironment()
      toEnv = association.toEnvironment()
      if (fromName not in self.conceptNameSet):
        self.buildNode(fromName,fromEnv)
        self.conceptNameSet.add(fromName)
      if (toName not in self.conceptNameSet):
        self.buildNode(toName,toEnv)
        self.conceptNameSet.add(fromName)

      conceptTriple = (fromName,toName,lbl)
      if (conceptTriple not in self.assocSet):
        self.theEdges.append(pydot.Edge(str(fromName),str(toName),label=str(lbl), fontname=self.fontName,fontsize=self.fontSize, arrowhead='vee',URL=fromName+ '#' + toName))

    for envName in self.theClusters:
      self.theGraph.add_subgraph(self.theClusters[envName])
    for edge in self.theEdges:
      self.theGraph.add_edge(edge)
    return self.layout()
