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

import json
import requests
import glob
import imghdr
import argparse
import os
import sys
import base64
if (sys.version_info > (3,)):
  from urllib.parse import quote
else:
  from urllib import quote


__author__ = 'Shamal Faily'

def authenticate(url,userName,passWd):
  credentials = 'Basic ' + base64.b64encode((userName + ':' + passWd).encode('ascii')).decode('ascii')
  resp = requests.post(url + '/api/session',headers={'Authorization': credentials})
  if not resp.ok:
    raise Exception('Authentication error' + resp.text)
  return resp.json()['session_id']


def importModelFile(importFile,url,dbName,createDb,overwrite,mFormat,userName,passWd):
  session = authenticate(url,userName,passWd)
  data = {'session_id':session}
  if (createDb):
    newDbResp = requests.post(url + '/api/settings/database/' + quote(dbName) + '/create',data=data)
    if not newDbResp.ok:
      exceptionTxt = 'Cannot create database ' + dbName + ': ' + newDbResp.text
      raise Exception(exceptionTxt)

  openDbResp = requests.post(url + '/api/settings/database/' + quote(dbName) + '/open',data=data)
  if not openDbResp.ok:
    exceptionTxt = 'Cannot open database ' + dbName + ': ' + openDbResp.text
    raise Exception(exceptionTxt)
  buf = open(importFile,'rb').read().decode('utf-8')
  import_json = {'session_id' : session,'object' : {'urlenc_file_contents':buf,'overwrite':overwrite,'type':mFormat}}
  hdrs = {'Content-type': 'application/json'}
  importResp = requests.post(url + '/api/import/text',data=json.dumps(import_json),headers=hdrs);
  if not importResp.ok:
    exceptionTxt = 'Cannot import ' + importFile + ': ' + importResp.text
    raise Exception(exceptionTxt)

def main(args=None):
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - Model Import using CAIRIS API')
  parser.add_argument('modelFile',help='model file to import')
  parser.add_argument('--url',dest='url',help='URL for CAIRIS server')
  parser.add_argument('--database',dest='dbName',default='cairis_default',help='database name')
  parser.add_argument('--user',dest='userName',default='test',help='Username')
  parser.add_argument('--password',dest='passWd',default='test',help='Password')
  parser.add_argument('--create',help='create flag',action="store_true")
  parser.add_argument('--overwrite',help='overwrite flag',action="store_true")
  parser.add_argument('--type',dest='modelFormat',help='model type to import.  One of securitypattern, attackpattern, tvtypes, directory, requirements, riskanalysis, usability, misusability, project, domainvalues, architecturalpattern, associations, synopses, processes, assets, locations, dataflows or all')
  args = parser.parse_args() 
  file_import(args.modelFile,args.url,args.dbName,args.create,args.overwrite,args.modelFormat,args.userName,args.passWd)

def file_import(importFile,url,dbName,createDb,overwrite,mFormat,userName,passWd):
  if (os.access(importFile, os.R_OK)) == False:
    raise Exception("Cannot access " + importFile)

  if (mFormat in ['securitypattern','attackpattern','tvtypes','directory','requirements','riskanalysis','usability', 'misusability','project','domainvalues','architecturalpattern','associations','synopses','processes','assets','locations','dataflows','all']):
    importModelFile(importFile,url,dbName,createDb,overwrite,mFormat,userName,passWd)
  else:
    raise Exception('Input model type ' + mFormat + ' not recognised')
  return 0

if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print("Fatal web_cimport error: " + str(e))
    sys.exit(-1)
