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
import jsonpickle
import glob
import imghdr
import argparse
from base64 import b64encode

import sys
if (sys.version_info > (3,)):
  from urllib.parse import quote
else:
  from urllib import quote

def authenticate(url,userName,passWd):
  credentials = 'Basic ' + b64encode((userName + ':' + passWd).encode('ascii')).decode('ascii')
  resp = requests.post(url + '/api/session',headers={'Authorization': credentials})
  if not resp.ok:
    raise Exception('Authentication error' + resp.text)
  return resp.json()['session_id']
  
def importModel(url,dbName,modelFile,session):
  data = {'session_id':session}
  newDbResp = requests.post(url + '/api/settings/database/' + quote(dbName) + '/create',data=data)
  if not newDbResp.ok:
    exceptionTxt = 'Cannot create database ' + dbName + ': ' + newDbResp.text
    raise Exception(exceptionTxt)
  importResp = requests.post(url + '/api/import/package?session_id=' + session,data=data,files=dict(file=open(modelFile,'rb')))
  if not importResp.ok:
    exceptionTxt = 'Cannot import ' + modelFile + ': ' + importResp.text
    raise Exception(exceptionTxt)

def main(args=None):
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - CAIRIS model import (using APIs)')
  parser.add_argument('modelFile',help='model file to import')
  parser.add_argument('--url',dest='url',help='URL for CAIRIS server')
  parser.add_argument('--database',dest='dbName',help='New database name')
  parser.add_argument('--user',dest='userName',default='test',help='Username')
  parser.add_argument('--password',dest='passWd',default='test',help='Password')
  args = parser.parse_args() 

  session = authenticate(args.url,args.userName,args.passWd)
  importModel(args.url,args.dbName,args.modelFile,session)

if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print('Fatal import error: ' + str(e))
    sys.exit(-1)
