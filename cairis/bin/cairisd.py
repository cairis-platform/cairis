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

__author__ = 'Shamal Faily'

import os
import sys
from cairis.daemon import create_app, db
from cairis.daemon.CairisHTTPError import CairisHTTPError
from cairis.bin.add_cairis_user import addAdditionalUserData
from flask_script import Manager, Server, Command
from flask_security import user_registered
from cairis.core.Borg import Borg

app = create_app()
manager = Manager(app)
manager.add_command('runserver', Server(host='0.0.0.0', port=7071))

@app.after_request
def apply_caching(response):
  response.headers["X-Frame-Options"] = "SAMEORIGIN"
  return response

@user_registered.connect_via(app)
def enroll(sender, user, confirm_token,form_data):
  addAdditionalUserData(user.email,user.password)

class TestClient(Command):
  def run(self):
    app.test_client()

manager.add_command('testclient', TestClient())

def main(args):
  manager.run()

if __name__ == '__main__':
  try:
    main(sys.argv)
  except CairisHTTPError as e:
    print('Fatal CAIRIS error: ' + str(e))
    sys.exit(-1)
