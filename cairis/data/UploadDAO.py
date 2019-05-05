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

import sys
if (sys.version_info > (3,)):
  import http.client
else:
  import httplib
import imghdr
import os
import io
from cairis.core.ARM import *
from werkzeug.datastructures import FileStorage
from cairis.core.Borg import Borg
from cairis.daemon.CairisHTTPError import CairisHTTPError
from cairis.data.CairisDAO import CairisDAO

__author__ = 'Robin Quetin, Shamal Faily'


class UploadDAO(CairisDAO):
  accepted_image_types = ['jpg', 'jpeg', 'png', 'bmp', 'gif']

  def __init__(self, session_id):
    CairisDAO.__init__(self, session_id)
    b = Borg()

  def set_image(self,name,content,mimeType):

    extension = os.path.splitext(name)
    img_format = imghdr.what(io.BytesIO(content))
    if not img_format or img_format not in self.accepted_image_types:
      raise CairisHTTPError(
              status_code=http.client.CONFLICT,
              status='Unsupported file type',
              message='The provided image file is not supported by CAIRIS'
      )

    try:
      self.db_proxy.setImage(name,content,mimeType)
    except ARMException as ex:
      self.close()
      raise ARMHTTPError(ex)
