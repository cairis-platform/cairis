#!/usr/bin/python
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
import base64

import sys
if (sys.version_info > (3,)):
  from urllib.parse import quote
else:
  from urllib import quote

def authenticate(url,userName,passWd):
  credentials = 'Basic ' + base64.b64encode((userName + ':' + passWd).encode('ascii')).decode('ascii')
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

  buf = open(modelFile,'rb').read().decode('utf-8')
  import_json = {'session_id' : session ,'object': {'urlenc_file_contents':buf,'overwrite': 1,'type':'all'}}
  hdrs = {'Content-type': 'application/json'}
  importResp = requests.post(url + '/api/import/text',data=json.dumps(import_json),headers=hdrs);
  if not importResp.ok:
    exceptionTxt = 'Cannot import ' + modelFile + ': ' + importResp.text
    raise Exception(exceptionTxt)

def importModelRichPicture(url,imgDir,imgFile,session):
  data = {'session_id':session}
  resp = requests.get(url + '/api/settings',data=data)
  if not resp.ok: 
    exceptionTxt = 'Cannot get project settings' + resp.text
    raise Exception(exceptionTxt)
  else:
    if (imghdr.what(imgDir + '/' + imgFile) == None):
      exceptionTxt = 'Error updating project settings: ' + imgFile + ' is an invalid image file.'
      raise Exception(exceptionTxt)
    settings = resp.json()
    imgResp = requests.post(url + '/api/upload/image',data=data,files=dict(file=open(imgDir + '/' + imgFile,'rb')))
    if not imgResp.ok:
      exceptionTxt = 'Error uploading ' + imgFile + ' :' + imgResp.text
      raise Exception(exceptionTxt)
    else:
      settings['richPicture'] = imgResp.json()['filename']
      settings_json = {'session_id' : session,'object' : settings}
      hdrs = {'Content-type': 'application/json'}
      settingsUpdResp = requests.put(url + '/api/settings',data=json.dumps(settings_json),headers=hdrs);
    if not settingsUpdResp.ok:
      exceptionTxt = 'Error updating project settings: ' + settingsUpdResp.text
      raise Exception(exceptionTxt)


def objectsWithImages(url,dimName,session):
  data = {'session_id':session}
  resp = requests.get(url + '/api/' + dimName + 's',data=data)
  if not resp.ok: 
    exceptionTxt = 'Cannot get ' + dimName + 's: ' + resp.text
    raise Exception(exceptionTxt)
  else:
    return resp.json()

def updateObjectImage(url,dimName,imgDir,objt,session):
  data = {'session_id':session}
  objtName = objt['theName']
  objtGlob = glob.glob(imgDir + '/' + objtName + '.*')
  if len(objtGlob) == 0:
    return
  elif len(objtGlob) > 1:
    exceptionTxt = 'Error uploading image for ' + objtName + ': expecting just 1 file for ' + objtName + ', but found ' + str(objtGlob) + '.'
    raise Exception(exceptionTxt)
  imgFile = objtGlob[0]
  if (imghdr.what(imgFile) == None):
    exceptionTxt = 'Error uploading ' + imgFile + ': invalid image file.'
    raise Exception(exceptionTxt)
  imgResp = requests.post(url + '/api/upload/image',data=data,files=dict(file=open(imgFile,'rb')))
  if not imgResp.ok:
    exceptionTxt = 'Error uploading ' + imgFile + ' :' + imgResp.text + '.'
    raise Exception(exceptionTxt)
  else:
    objt['theImage'] = imgResp.json()['filename']
    objt_json = {'session_id' : session,'object' : objt}
    hdrs = {'Content-type': 'application/json'}
    objtUpdResp = requests.put(url + '/api/' + dimName + 's/name/' + objtName,data=json.dumps(objt_json),headers=hdrs);
    if not objtUpdResp.ok:
      exceptionTxt = 'Error updating ' + objtName + ': ' + objtUpdResp.text + '.'
      raise Exception(exceptionTxt)

def main(args=None):
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - CAIRIS model import (using APIs)')
  parser.add_argument('modelFile',help='model file to import')
  parser.add_argument('--url',dest='url',help='URL for CAIRIS server')
  parser.add_argument('--database',dest='dbName',help='New database name')
  parser.add_argument('--user',dest='userName',default='test',help='Username')
  parser.add_argument('--password',dest='passWd',default='test',help='Password')
  parser.add_argument('--image_dir',dest='imageDir',default='',help='Directory for model images')
  parser.add_argument('--rich_pic',dest='rpImage',default='',help='Rich picture image file')
  args = parser.parse_args() 

  session = authenticate(args.url,args.userName,args.passWd)
  importModel(args.url,args.dbName,args.modelFile,session)
  if (args.imageDir != '' and args.rpImage != ''):
    importModelRichPicture(args.url,args.imageDir,args.rpImage,session)

  if (args.imageDir != ''):
    personaObjts = objectsWithImages(args.url,'persona',session)
    for pName in list(personaObjts.keys()):
      updateObjectImage(args.url,'persona',args.imageDir,personaObjts[pName],session)
    attackerObjts = objectsWithImages(args.url,'attacker',session)
    for aName in list(attackerObjts.keys()):
      updateObjectImage(args.url,'attacker',args.imageDir,attackerObjts[aName],session)

if __name__ == '__main__':
  try:
    main()
  except Exception as e:
    print('Fatal import error: ' + str(e))
    sys.exit(-1)
