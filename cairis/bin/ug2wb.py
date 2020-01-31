#!/usr/bin/python3
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

import argparse
from xlsxwriter import Workbook
import cairis.core.BorgFactory
from cairis.core.Borg import Borg


__author__ = 'Shamal Faily'

def main(args=None):
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Persona characteristics To Workbook converter')
  parser.add_argument('xlsxFile',help='Workbook to create')
  parser.add_argument('--user',dest='userName',help='user name', default='cairis_test')
  parser.add_argument('--database',dest='dbName',help='database name',default='cairis_test')
  args = parser.parse_args()

  cairis.core.BorgFactory.initialise(user=args.userName,db=args.dbName)
  b = Borg()
  drs = b.dbProxy.getDocumentReferences()
  pcs = list(map(lambda x: x[1],list(b.dbProxy.getPersonaCharacteristics().items())))
 
  drSet = set([])
  for pc in pcs:
    personaName = pc.persona()
    for e in pc.grounds() + pc.warrant() + pc.rebuttal():
      dr = drs[e[0]] 
      dr.thePersonaName = personaName
      drSet.add(dr)
    
  wb = Workbook(args.xlsxFile)
  ugSheet = wb.add_worksheet('UserGoal')
  hFormat = wb.add_format({'border':1,'bg_color' : '#C6EFCE', 'bold' : True, 'text_wrap' : True})
  unlocked = wb.add_format({'locked': False,'text_wrap' : True,'font_color' : 'green'})
  tWrap = wb.add_format({'text_wrap' : True,'italic' : True})
  ugSheet.protect()
  ugSheet.write('A1','Reference',hFormat)
  ugSheet.write('B1','Description',hFormat)
  ugSheet.write('C1','Persona',hFormat)
  ugSheet.write('D1','persona/document_reference',hFormat)
  ugSheet.write('E1','Element Type',hFormat)
  ugSheet.write('F1','User Goal',hFormat)
  ugSheet.write('G1','Initial Satisfaction',hFormat)

  cellDict = {}
  ugRow = 1
  for objt in pcs + list(drSet):
    refName = ''
    elementType = ''
    refDesc = ''
    if (objt.__class__.__name__ == 'PersonaCharacteristic'):
      refName = objt.characteristic()
      elementType = 'persona'
      refDesc = refName
    else:
      refName = objt.name()
      elementType = 'document_reference'
      refDesc = objt.excerpt()
    ugSheet.write_string(ugRow,0,refName,tWrap)
    ugSheet.write_string(ugRow,1,refDesc,tWrap)
    ugSheet.write_string(ugRow,2,objt.thePersonaName,tWrap)
    ugSheet.write_string(ugRow,3,elementType,tWrap)
    ugSheet.data_validation('E' + str(ugRow),{'validate':'list','source' : ['goal','softgoal','belief']})
    ugSheet.write_string('E' + str(ugRow + 1),'goal',unlocked)
    cellDict[refName] = 'F' + str(ugRow + 1)
    ugSheet.write_string(ugRow,5,'',unlocked)
    ugSheet.data_validation('G' + str(ugRow + 1),{'validate':'list','source' : ['Satisfied','Weakly Satisfied','None','Weakly Denied','Denied']}) 
    ugSheet.write_string('G' + str(ugRow + 1),'None',unlocked)
    ugRow += 1
  ugSheet.set_column('A:B',30)
  ugSheet.set_column('C:D',20)
  ugSheet.set_column('F:G',30)

  contSheet = wb.add_worksheet('Contributions')
  hFormat = wb.add_format({'border':1,'bg_color' : '#C6EFCE', 'bold' : True, 'text_wrap' : True})
  contSheet.protect()
  contSheet.write('A1','Source (GWR User Goal)',hFormat)
  contSheet.write('B1','Destination (PC User Goal)',hFormat)
  contSheet.write('C1','Means/End',hFormat)
  contSheet.write('D1','Contribution',hFormat)

  contRow = 1
  for pc in pcs:
    for e in pc.grounds() + pc.warrant() + pc.rebuttal():
      contSheet.write_formula(contRow,0,"=UserGoal!" + cellDict[e[0]],tWrap)
      contSheet.write_formula(contRow,1,"=UserGoal!" + cellDict[pc.characteristic()],tWrap)
      contSheet.data_validation('C' + str(contRow + 1),{'validate':'list','source' : ['means','end']})
      contSheet.write('C' + str(contRow + 1),'means',unlocked)
      contSheet.data_validation('D' + str(contRow + 1),{'validate':'list','source' : ['Make','SomePositive','Help','Hurt','SomeNegative','Break']})
      contSheet.write('D' + str(contRow + 1),'Help',unlocked)
      contRow +=1 
  contSheet.set_column('A:B',20)
  contSheet.set_column('C:D',15)

  wb.close()
if __name__ == '__main__':
  main()
