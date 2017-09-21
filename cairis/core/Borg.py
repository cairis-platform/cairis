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

__author__ = 'Shamal Faily, Robin Quetin'

from random import choice
import string
from time import sleep
from .ARM import SessionNotFound

class Borg:
  __shared_state = {}
  def __init__(self):
    self.__dict__ = self.__shared_state

  def get_dbproxy(self, id=None):
    if self.runmode == 'desktop':
      if self.dbProxy is not None:
        return self.dbProxy
    elif self.runmode == 'web':
      if id is None:
        raise RuntimeError('No ID provided while run mode is "web"')
      else:
        settings = self.get_settings(id)
        if settings is not None:
          return settings.get('dbProxy', None)
        else:
          raise SessionNotFound(id)
    else:
      return None

  def init_settings(self):
    """
    Creates a new settings dictionary in the Borg instance and returns the identifier for the settings dictionary
    :rtype : str
    """
    random_id = ''.join(choice(string.ascii_letters+string.digits) for i in range(32))
    while random_id in self.settings:
      sleep(40)
      ''.join(choice(string.ascii_letters+string.digits) for i in range(32))

    self.settings[random_id] = {'session_id': random_id}
    return random_id

  def get_settings(self, session_id):
    if session_id in self.settings:
      return self.settings[session_id]
    else:
      return None
