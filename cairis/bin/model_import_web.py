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
from urllib import quote
import sys

def importModel(url,modelFile):
  buf = open(modelFile,'rb').read()
  import_json = {'session_id' : 'test','object' : {'urlenc_file_contents':buf,'type':'all'}}
  hdrs = {'Content-type': 'application/json'}
  resp = requests.post(url + '/api/import/text',data=json.dumps(import_json),headers=hdrs);
  if not resp.ok:
    exceptionTxt = 'Cannot import ' + modelFile + ': ' + resp.text
    raise Exception(exceptionTxt)

def importModelRichPicture(url,imgDir,imgFile):
  resp = requests.get(url + '/api/settings?session_id=test')
  if not resp.ok: 
    exceptionTxt = 'Cannot get project settings' + resp.text
    raise Exception(exceptionTxt)
  else:
    if (imghdr.what(imgDir + '/' + imgFile) == None):
      exceptionTxt = 'Error updating project settings: ' + imgFile + ' is an invalid image file.'
      raise Exception(exceptionTxt)
    settings = resp.json()
    imgResp = requests.post(url + '/api/upload/image?session_id=test',files=dict(file=open(imgDir + '/' + imgFile,'rb')))
    if not imgResp.ok:
      exceptionTxt = 'Error uploading ' + imgFile + ' :' + imgResp.text
      raise Exception(exceptionTxt)
    else:
      settings['richPicture'] = imgResp.json()['filename']
      settings_json = {'session_id' : 'test','object' : settings}
      hdrs = {'Content-type': 'application/json'}
      settingsUpdResp = requests.put(url + '/api/settings',data=json.dumps(settings_json),headers=hdrs);
    if not settingsUpdResp.ok:
      exceptionTxt = 'Error updating project settings: ' + settingsUpdResp.text
      raise Exception(exceptionTxt)


def objectsWithImages(url,dimName):
  resp = requests.get(url + '/api/' + dimName + 's?session_id=test')
  if not resp.ok: 
    exceptionTxt = 'Cannot get ' + dimName + 's: ' + resp.text
    raise Exception(exceptionTxt)
  else:
    return resp.json()

def updateObjectImage(url,dimName,imgDir,objt):
  objtName = objt['theName']
  objtGlob = glob.glob(imgDir + '/' + objtName + '.*')
  if len(objtGlob) != 1:
    exceptionTxt = 'Error uploading image for ' + objtName + ': expecting just 1 file for ' + objtName + ', but found ' + str(objtGlob) + '.'
    raise Exception(exceptionTxt)
  imgFile = objtGlob[0]
  if (imghdr.what(imgFile) == None):
    exceptionTxt = 'Error uploading ' + imgFile + ': invalid image file.'
    raise Exception(exceptionTxt)
  imgResp = requests.post(url + '/api/upload/image?session_id=test',files=dict(file=open(imgFile,'rb')))
  if not imgResp.ok:
    exceptionTxt = 'Error uploading ' + imgFile + ' :' + imgResp.text + '.'
    raise Exception(exceptionTxt)
  else:
    objt['theImage'] = imgResp.json()['filename']
    objt_json = {'session_id' : 'test','object' : objt}
    hdrs = {'Content-type': 'application/json'}
    objtUpdResp = requests.put(url + '/api/' + dimName + 's/name/' + objtName,data=json.dumps(objt_json),headers=hdrs);
    if not objtUpdResp.ok:
      exceptionTxt = 'Error updating ' + objtName + ': ' + objtUpdResp.text + '.'
      raise Exception(exceptionTxt)

def main(args=None):
  parser = argparse.ArgumentParser(description='Computer Aided Integration of Requirements and Information Security - CAIRIS model import (using APIs)')
  parser.add_argument('modelFile',help='model file to import')
  parser.add_argument('--url',dest='url',help='URL for CAIRIS server')
  parser.add_argument('--image_dir',dest='imageDir',help='Directory for model images')
  parser.add_argument('--rich_pic',dest='rpImage',help='Rich picture image file')
  args = parser.parse_args() 

  importModel(args.url,args.modelFile)
  importModelRichPicture(args.url,args.imageDir,args.rpImage)
  personaObjts = objectsWithImages(args.url,'persona')
  for pName in personaObjts.keys():
    updateObjectImage(args.url,'persona',args.imageDir,personaObjts[pName])
  attackerObjts = objectsWithImages(args.url,'attacker')
  for aName in attackerObjts.keys():
    updateObjectImage(args.url,'attacker',args.imageDir,attackerObjts[aName])

if __name__ == '__main__':
  try:
    main()
  except Exception, e:
    print 'Fatal import error: ' + str(e)
    sys.exit(-1)
